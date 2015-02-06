from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

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
              <button type='button' id='f' class='btn btn-default'><span class='fa fa-users'></span> Fan</button>\
              <button type='button' id='m' class='btn btn-default'><span class='fa fa-music'></span> Artist</button>\
              <button type='button' id='v' class='btn btn-default'><span class='fa fa-ticket'></span> Venue</button>\
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

    def clean_band_name(self):
        band_name = self.cleaned_data.get('band_name')
        if self.cleaned_data.get('profile_type') == 'm':
            if not band_name:
                raise forms.ValidationError(_(u"A band name is required for Artists."))
        return band_name

    def clean_venue_name(self):
        venue_name = self.cleaned_data.get('venue_name')
        if self.cleaned_data.get('profile_type') == 'v':
            if not venue_name:
                raise forms.ValidationError(_(u"A venue name is required for Venues."))
        return venue_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if self.cleaned_data.get('profile_type') == 'f':
            if not first_name:
                raise forms.ValidationError(_(u"A first name is required for Fans."))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if self.cleaned_data.get('profile_type') == 'f':
            if not last_name:
                raise forms.ValidationError(_(u"A last name is required for Fans."))
        return last_name

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
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = get_object_or_None(User, email=email)
        if user:
            try:
                hasowner = user.profile.has_owner
            except:
                hasowner = True
            if hasowner:
                raise forms.ValidationError(_(u"This email is already in use. Please supply a different email."))
            else:
                raise forms.ValidationError(
                    (_(mark_safe(('An account fo this email already exists, click <a href="{0}">Here</a> to claim this account.')
                        .format(reverse('claim_profile_verify', kwargs={'username': user.username})))))
                )
        return email

class ClaimProfileForm(SetPasswordForm):
    def __init__(self, data=None, *args, **kw):
        super(ClaimProfileForm, self).__init__(data, *args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
              Div('new_password1',css_class='col-sm-6 left',),
              Div('new_password2',css_class='col-sm-6 right',),
              css_class='row no-gutter',
            ),
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
