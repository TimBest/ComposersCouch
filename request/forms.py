from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm
from autocomplete_light import ChoiceWidget, MultipleChoiceWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

from . import models
from accounts.models import MusicianProfile
from annoying.functions import get_object_or_None
from contact.models import Zipcode
from schedule.forms import DateForm, UserSelectForm
from schedule.models import DateRange


class DateForm(DateForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
              Div('start',css_class='col-xs-6 left',),
              Div('end',css_class='col-xs-6 right',css_id='end-div',),
              css_class='row no-gutter',
            ),
      )

class MessageForm(forms.Form):
    body = forms.CharField(label=_("Message"),
              widget=forms.Textarea(attrs={'rows': 2, 'cols': 19}))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('body',)

class RequestForm(ModelForm):
    date_format = '%m/%d/%Y'
    accept_by = forms.DateField(label=_("Accept by"),
                                widget=forms.DateInput(format=date_format))

    class Meta:
        model = models.Request
        fields = ('accept_by',)

class PrivateRequestForm(RequestForm, UserSelectForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PrivateRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            self.participants,
            'accept_by',
        )

    class Meta:
        model = models.PrivateRequest
        fields = ('accept_by','headliner','host','openers',)

    def clean(self):
        # user must be a participent in the evnet or request
        isParticipent = False
        try:
            if self.cleaned_data.get('headliner').profile.user == self.user:
                isParticipent = True
        except:
            pass
        if self.cleaned_data.get('host') == self.user:
            isParticipent = True
        else:
            for o in self.cleaned_data.get('openers'):
                if o.profile.user == self.user:
                    isParticipent = True
        if not isParticipent:
            raise forms.ValidationError(_(u"You must be part of this request"))
        return super(PrivateRequestForm, self).clean()

class EditPrivateRequestForm(RequestForm):

    def __init__(self, *args, **kw):
      super(EditPrivateRequestForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
          'accept_by',
      )
    class Meta:
        model = models.PrivateRequest
        fields = ('accept_by',)

class PublicRequestForm(RequestForm):

    def __init__(self, *args, **kw):
      super(PublicRequestForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
          'zip_code',
          'details',
          'accept_by',
      )

    class Meta:
        model = models.PublicRequest
        widgets = {
          'details' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('accept_by','details', 'zip_code',)

class NumberOfApplicantsForm(PublicRequestForm):

    def __init__(self, *args, **kw):
      super(NumberOfApplicantsForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout('total',)

    class Meta:
        model = models.NumberOfApplicants
        fields = ('total',)

class AcceptForm(forms.Form):

    class Meta:
        model = models.Accept

    def save(self, user, private_request, accepted):
        a = get_object_or_None(models.Accept, user=user.id, request=private_request.id)
        if a:
            a.accepted = accepted
        else:
            a = models.Accept.objects.create(
                user=user,
                request=private_request,
                accepted=accepted,
            )
        a.save()
        return a

class ApproveForm(forms.Form):

    class Meta:
        model = models.Application

    def save(self, application, approved):
        application.approved = approved
        public_request = application.public_request
        if hasattr(public_request, 'applicants'):
            applicants = public_request.applicants
            # TODO: fix this logic while still allowing users
            if approved and applicants.left > 0:
                applicants.left = applicants.left - 1
            else:
                applicants.left = applicants.left + 1
        else:
            if approved == True:
                public_request = True
            else:
                public_request = False
        public_request.save()
        application.save()
        return application
