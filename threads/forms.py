from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm
from autocomplete_light import MultipleChoiceWidget

from threads.models import *
from threads.utils import reply_to_thread, now
from threads.signals import message_composed


WRAP_WIDTH = 55

class ComposeForm(ModelForm):
    """
    A simple default form for private messages.
    """
    recipients = forms.ModelMultipleChoiceField(User.objects.all(),
                    widget=MultipleChoiceWidget('UserAutocomplete',))
    subject = forms.CharField(label=_(u"Subject"))

    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'cols': WRAP_WIDTH, 'rows': 3}),
        }

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
            Participant.objects.get_or_create(thread=thread, user=recipient)

        (sender_part, created) = Participant.objects.get_or_create(thread=thread, user=sender)
        sender_part.replied_at = sender_part.read_at = now()
        sender_part.save()

        thread.save()  # save this last, since this updates the search index
        message_composed.send(sender=Message, message=new_message,recipients=recipients)
        return (thread, new_message)


class ReplyForm(forms.Form):
    """
    A simple default form for private messages.
    """
    body = forms.CharField(label=_(u"Reply"),
        widget=forms.Textarea(attrs={'rows': '4', 'cols': '55'}))

    def save(self, sender, thread):
        body = self.cleaned_data['body']
        return reply_to_thread(thread, sender, body)
