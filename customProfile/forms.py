from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import autocomplete_light
from crispy_forms.bootstrap import FormActions, InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Layout, Submit

from accounts import models
from annoying.functions import get_object_or_None
from customProfile.musician.models import Member, Instrument
from photos.forms import MugshotForm
from genres.models import Genre


class MusicianProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        try:
            required = kwargs.pop('required')
        except:
            required = True
        super(MusicianProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('name',)
        self.fields['name'].required = required

    class Meta:
        model = models.MusicianProfile
        fields = ('name',)


class VenueProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        try:
            required = kwargs.pop('required')
        except:
            required = True
        super(VenueProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('name',)
        self.fields['name'].required = required

    class Meta:
        model = models.VenueProfile
        fields = ('name',)

class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        try:
            required = kwargs.pop('required')
        except:
            required = True
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
          Div(
            Div('first_name',css_class='col-sm-6 left',),
            Div('last_name',css_class='col-sm-6 right',),
            css_class='row no-gutter',
          ),
        )
        self.fields['first_name'].required = required
        self.fields['last_name'].required = required

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name')

class UsernameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UsernameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['username'].help_text = "This will appear at the end of your profile's URL"
        self.fields['username'].label = "Slug"
        self.fields['email'].required = True
        self.helper.layout = Layout('email', 'username',)


    class Meta:
        model = models.User
        fields = ('email', 'username',)

class ProfileForm(autocomplete_light.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('genre',)

    class Meta:
        model = models.Profile
        fields = ('genre',)

class ProfileTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(InlineRadios('profile_type'),)

    class Meta:
        model = models.Profile
        fields = ('profile_type',)
