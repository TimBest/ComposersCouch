from django import forms
from django.contrib.auth.models import User
from django.forms.models import BaseModelFormSet
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

class ParticipantFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ParticipantFormSet, self).__init__(*args, **kwargs)

    @cached_property
    def forms(self):
        """
        Instantiate forms at first property access.
        """
        # DoS protection is included in total_form_count()
        forms = [self._construct_form(i, user=self.user) for i in xrange(self.total_form_count())]
        return forms

class ParticipantForm(ModelForm):
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

    class Meta:
        model = Participant
        fields = ('user',)

    def clean(self):
        email = self.cleaned_data.get('email')
        user = self.cleaned_data.get('user')
        if not email and not user :
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
        participant = super(ParticipantForm, self).save(commit=False)
        participant.thread = thread
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
        self.user = kwargs.pop('user')
        self.profile_type = 'm'
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div('id',css_class='hidden',),
            'user',
            Div(
              Div(Field('name',placeholder='Name'),css_class='col-xs-6 left',),
              Div(Field('email',placeholder='Email'),css_class='col-xs-6 right',),
              css_class='row no-gutter',
            ),
        )

    class Meta:
        model = Participant
        fields = ('id','user',)

class RequestForm(ModelForm):
    date_format = '%m/%d/%Y'
    accept_by = forms.DateField(label=_("Accept by"), required=False,
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

class AcceptForm(forms.Form):

    class Meta:
        model = models.RequestParticipant

    """def save(self, user, private_request, accepted):
        a = get_object_or_None(models.RequestParticipant, user=user.id, request=private_request.id)
        if a:
            a.accepted = accepted
        else:
            a = models.Accept.objects.create(
                user=user,
                request=private_request,
                accepted=accepted,
            )
        a.save()
        return a"""

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
