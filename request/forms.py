from django import forms
from django.contrib.auth.models import User
from django.forms.formsets import BaseFormSet
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm, ChoiceWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

from . import models
from accounts.models import MusicianProfile
from accounts.utils import create_user_profile
from annoying.functions import get_object_or_None
from contact.models import Zipcode
from schedule.forms import DateForm, UserSelectForm
from schedule.models import DateRange
from threaded_messages.models import Participant


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
    body = forms.CharField(label=_("Details"),
              widget=forms.Textarea(attrs={'rows': 2, 'cols': 19}))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('body',)

class ParticipantFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ParticipantFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.forms[0].cleaned_data
        if not cleaned_data.get('email') and not cleaned_data.get('user'):
            raise forms.ValidationError(_(u"At least one user or email is required"))

    @cached_property
    def forms(self):
        """
        Instantiate forms at first property access.
        """
        # DoS protection is included in total_form_count()
        forms = [self._construct_form(i, user=self.user) for i in xrange(self.total_form_count())]
        return forms

class ParticipantForm(forms.Form):
    user = forms.ModelChoiceField(User.objects.all(), required=False,
                widget=ChoiceWidget('UserAutocomplete',))
    email = forms.EmailField(required=False)
    name = forms.CharField(max_length=64, required=False)
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.profile_type = 'v'
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'user',
            Div(
              Div(Field('name',placeholder='Name'),css_class='col-xs-6 left',),
              Div(Field('email',placeholder='Email'),css_class='col-xs-6 right',),
              css_class='row no-gutter',
            ),
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        user = self.cleaned_data.get('user')
        if not email and not user:
            raise forms.ValidationError(_(u"A user or email is required"))
        if email and not user:
            user = get_object_or_None(User, email=email)
            if not user:
                name = self.cleaned_data.get('name')
                if not name:
                    name = email
                user = create_user_profile(name=name, email=email,
                            profile_type=self.profile_type, creator=self.user)
            self.cleaned_data['user']=user
            return self.cleaned_data

    def save(self, thread, sender, role='o'):
        participant, created = Participant.objects.get_or_create(user=self.cleaned_data['user'],thread=thread)
        participant.save()
        request_paticipant = models.RequestParticipant(participant=participant, role=role)
        if participant.user == sender:
            participant.read_at = now()
            participant.replied_at = now()
            participant.save()
            request_paticipant.accepted = True
        request_paticipant.save()
        return participant

class ArtistParticipantForm(ParticipantForm):
    user = forms.ModelChoiceField(User.objects.all(), required=False,
                widget=ChoiceWidget('UserArtistAutocomplete',))

    def __init__(self, *args, **kwargs):
        self.profile_type = 'm'
        super(ArtistParticipantForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        user = self.cleaned_data.get('user')
        if email and not user:
            user = get_object_or_None(User, email=email)
            if not user:
                name = self.cleaned_data.get('name')
                if not name:
                    name = email
                user = create_user_profile(name=name, email=email,
                            profile_type=self.profile_type, creator=self.user)
            self.cleaned_data['user']=user
            return self.cleaned_data

class RequestForm(ModelForm):
    date_format = '%m/%d/%Y'
    accept_by = forms.DateField(label=_("Application deadline"), required=False,
                                widget=forms.DateInput(format=date_format))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RequestForm, self).__init__(*args, **kwargs)
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
