from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from accounts.models import PROFILE_TYPE_CHOICES, Profile
from annoying.functions import get_object_or_None
from userena.forms import SignupFormOnlyEmail


class SignupForm(forms.ModelForm):
    FAN = PROFILE_TYPE_CHOICES[0][1]
    MUSICIAN = PROFILE_TYPE_CHOICES[1][1]
    VENUE = PROFILE_TYPE_CHOICES[2][1]

    first_name = forms.CharField(label=_(u'First name'), max_length=64,
                                 required=False)
    last_name = forms.CharField(label=_(u'Last name'), max_length=64,
                                required=False)
    band_name = forms.CharField(label=_(u'Band name'), max_length=64,
                                required=False)
    venue_name = forms.CharField(label=_(u'Venue name'), max_length=64,
                                 required=False)
    def __init__(self, data=None, *args, **kwargs):
        super(SignupForm, self).__init__(data, *args, **kwargs)
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
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
    MIN_LENGTH = 5

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)
        return password1
