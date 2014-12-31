import settings as sendgrid_settings
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm
from autocomplete_light import MultipleChoiceWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit

from .models import *
from .utils import reply_to_thread, now
from .signals import message_composed

if sendgrid_settings.MESSAGES_USE_SENDGRID:
    from sendgrid_parse_api.utils import create_reply_email


notification = None
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
WRAP_WIDTH = 55

class ComposeForm(ModelForm):
    """
    A simple default form for private messages.
    """
    recipients = forms.ModelMultipleChoiceField(
              User.objects.all(),
              widget=MultipleChoiceWidget('UserAutocomplete',))
    subject = forms.CharField(label=_(u"Subject"))

    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'cols': WRAP_WIDTH, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ComposeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'recipients',
            'subject',
            'body',
        )

    def save(self, sender, send=True):
        recipients = self.cleaned_data['recipients']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']

        new_message = Message.objects.create(body=body, sender=sender)

        thread = Thread.objects.create(subject=subject,
                                       latest_msg=new_message,
                                       creator=sender)
        thread.all_msgs.add(new_message)

        for recipient in recipients:
            Participant.objects.create(thread=thread, user=recipient)

        (sender_part, created) = Participant.objects.get_or_create(thread=thread, user=sender)
        sender_part.replied_at = sender_part.read_at = now()
        sender_part.save()

        thread.save()  # save this last, since this updates the search index

        message_composed.send(sender=Message,
                              message=new_message,
                              recipients=recipients)

        #send notifications
        if send and notification:
            if sendgrid_settings.MESSAGES_USE_SENDGRID:
                for r in recipients:
                    reply_email = create_reply_email(sendgrid_settings.MESSAGES_ID, r, thread)
                    notification.send(recipients, "received_email",
                                        {"thread": thread,
                                         "message": new_message}, sender=sender,
                                        from_email=reply_email.get_from_email(),
                                        headers={'Reply-To': reply_email.get_reply_to_email()})
            else:
                notification.send(recipients, "received_email",
                                        {"thread": thread,
                                         "message": new_message}, sender=sender)

        return (thread, new_message)


class ReplyForm(forms.Form):
    """
    A simple default form for private messages.
    """
    body = forms.CharField(label=_(u"Reply"),
        widget=forms.Textarea(attrs={'rows': '4', 'cols': '55'}))

    def __init__(self, instance=None, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('body',)
        self.fields['body'].label = False

    def save(self, sender, thread):
        body = self.cleaned_data['body']
        return reply_to_thread(thread, sender, body)
