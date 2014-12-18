from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from crispy_forms.bootstrap import FormActions, InlineRadios, InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, HTML, Layout, Submit

from pipeline import create_profile
from models import PROFILE_TYPE_CHOICES
from models import Profile, FanProfile, MusicianProfile, VenueProfile
from annoying.functions import get_object_or_None
from contact.forms import ZipcodeForm
from userena.forms import SignupFormOnlyEmail, AuthenticationForm


profile_type = Layout(
    HTML(
        "<div class='profile-type form-group' style='display:none;'>\
          <label for='id_profile_type' class='control-label  requiredField'>Profile type<span class='asteriskField'>*</span></label>\
          <div><div class='btn-group' role='group'>\
              <button type='button' id='f' class='btn btn-default'>Fan</button>\
              <button type='button' id='m' class='btn btn-default'>Musician</button>\
              <button type='button' id='v' class='btn btn-default'>Venue</button>\
          </div></div>\
        </div>"
    )
)

class SignupForm(forms.ModelForm):
    FAN = PROFILE_TYPE_CHOICES[0][1]
    MUSICIAN = PROFILE_TYPE_CHOICES[1][1]
    VENUE = PROFILE_TYPE_CHOICES[2][1]

    first_name = forms.CharField(label=_(u'First name'),
                                 max_length=64,
                                 required=False)
    last_name = forms.CharField(label=_(u'Last name'),
                                max_length=64,
                                required=False)
    band_name = forms.CharField(label=_(u'Band name'),
                                 max_length=64,
                                 required=False)
    venue_name = forms.CharField(label=_(u'Venue name'),
                                 max_length=64,
                                 required=False)
    def __init__(self, data=None, *args, **kwargs):
        super(SignupForm, self).__init__(data, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                profile_type,
                InlineRadios('profile_type'),
                Div(
                  Div('first_name',css_class='col-sm-6 left',),
                  Div('last_name',css_class='col-sm-6 right',),
                  css_class='row no-gutter',
                ),
                'band_name',
                'venue_name',
            ),
        )
        if data and data.get('profile_type', None) == self.FAN:
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
        elif data and data.get('profile_type', None) == self.MUSICIAN:
            self.fields['band_name'].required = True
        elif data and data.get('profile_type', None) == self.VENUE:
            self.fields['venue_name'].required = True

    class Meta:
        model = Profile
        fields = ('profile_type',)

class EmailForm(SignupFormOnlyEmail):

    def __init__(self, data=None, *args, **kw):
        super(EmailForm, self).__init__(data, *args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'email',
            Div(
              Div('password1',css_class='col-sm-6 left',),
              Div('password2',css_class='col-sm-6 right',),
              css_class='row no-gutter',
            ),
        )

attrs_dict = {'class': 'required'}

class CreateUserForm(forms.Form):
    email = forms.EmailField(label=_("Email"),
                             widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)))
    def __init__(self, data=None, *args, **kw):
        super(CreateUserForm, self).__init__(data, *args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'email',
        )

class SigninForm(AuthenticationForm):

    def __init__(self, data=None, *args, **kw):
        super(SigninForm, self).__init__(data, *args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'identification',
            'password',
            Div(
              Div('remember_me',css_class='col-xs-6 left',),
              Div(
                HTML("<a href='{% url 'userena_password_reset' %}' class='text-right checkbox'>Forgot your password?</a>"),
                css_class='col-xs-6 right',
              ),
              css_class='row no-gutter',
            ),
        )
        self.fields['remember_me'].label = _(u'Remember me')
