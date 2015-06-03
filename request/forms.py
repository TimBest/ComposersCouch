from django import forms
from django.contrib.auth.models import User
from django.forms.formsets import BaseFormSet
from django.utils.functional import cached_property
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm, ChoiceWidget

from . import models
from accounts.utils import create_user_profile
from annoying.functions import get_object_or_None
from schedule.forms import DateForm
from threads.models import Participant


class DateForm(DateForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DateForm, self).__init__(*args, **kwargs)

    def clean(self):
        start = self.cleaned_data['start']
        end = self.cleaned_data.get('end',None)
        if start and end:
            if end < start:
                raise forms.ValidationError(_(u"The end time must be later than start time."))
        if start.date() < timezone.now().date():
            raise forms.ValidationError(_(u"The start time must after today."))
        return self.cleaned_data

class MessageForm(forms.Form):
    body = forms.CharField(label=_("Details"),
              widget=forms.Textarea(attrs={'rows': 2, 'cols': 19}))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)

class ParticipantFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ParticipantFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.forms[0].cleaned_data
        if not cleaned_data.get('email') and not cleaned_data.get('participant'):
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
    participant = forms.ModelChoiceField(User.objects.all(), label=_("Venue"),
                required=False, widget=ChoiceWidget('UserAutocomplete',))
    email = forms.EmailField(required=False)
    name = forms.CharField(max_length=64, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ParticipantForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        user = self.cleaned_data.get('participant')
        if not email and not user:
            raise forms.ValidationError(_(u"A user or email is required."))
        if email and not user:
            user = get_object_or_None(User, email=email)
            if not user:
                name = self.cleaned_data.get('name')
                if not name:
                    name = email
                user = create_user_profile(name=name, email=email,
                            profile_type='v', creator=self.user)
            self.cleaned_data['participant']=user
            return self.cleaned_data

    def save(self, thread, sender, role='o'):
        participant, created = Participant.objects.get_or_create(user=self.cleaned_data['participant'],thread=thread)
        participant.save()
        request_paticipant = models.RequestParticipant(participant=participant, role=role)
        if participant.user == sender:
            participant.read_at = timezone.now()
            participant.replied_at = timezone.now()
            participant.save()
            request_paticipant.accepted = True
        request_paticipant.save()
        return participant

class ArtistParticipantForm(ParticipantForm):
    participant = forms.ModelChoiceField(User.objects.all(), label=_("Artist"),
                required=False, widget=ChoiceWidget('UserArtistAutocomplete',))

    def __init__(self, *args, **kwargs):
        super(ArtistParticipantForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        user = self.cleaned_data.get('participant')
        if email and not user:
            user = get_object_or_None(User, email=email)
            if not user:
                name = self.cleaned_data.get('name')
                if not name:
                    name = email
                user = create_user_profile(name=name, email=email,
                            profile_type='m', creator=self.user)
            self.cleaned_data['participant']=user
            return self.cleaned_data

class PublicRequestForm(ModelForm):
    date_format = '%m/%d/%Y'
    accept_by = forms.DateField(label=_("Application deadline"),
                                widget=forms.DateInput(format=date_format))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PublicRequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.PublicRequest
        widgets = {
          'details' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('zip_code','details', 'accept_by',)

    def clean_accept_by(self):
        accept_by = self.cleaned_data['accept_by']
        if accept_by < timezone.now().date():
            raise forms.ValidationError(_(u"There must be time to accept the request."))
        return accept_by

class NumberOfApplicantsForm(ModelForm):

    def __init__(self, *args, **kw):
      super(NumberOfApplicantsForm, self).__init__(*args, **kw)

    class Meta:
        model = models.NumberOfApplicants
        fields = ('total',)

class ApproveForm(forms.Form):

    class Meta:
        model = models.Application

    def save(self, application, approved):
        public_request = application.public_request
        if hasattr(public_request, 'applicants'):
            applicants = public_request.applicants
            # if application is approved and there and slots left
            if approved and applicants.left > 0:
                applicants.left = applicants.left - 1
            # if application was approved and no longer is
            elif not approved and application.approved:
                applicants.left = applicants.left + 1
            # if there are not applications left
            if applicants.left >= 0:
                public_request.fulfilled = True
            else:
                public_request.fulfilled = False
            public_request.applicants.save()
        else:
            # public request has no applicants model (therefor can only accet one user)
            if approved == True:
                public_request.fulfilled = True
            else:
                public_request.fulfilled = False
        public_request.save()
        application.approved = approved
        application.save()
        return application
