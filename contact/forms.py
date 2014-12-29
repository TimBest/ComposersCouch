from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _

from autocomplete_light.forms import ModelForm, ChoiceWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit

from models import Location, Contact, Zipcode, MusicLinks, SocialLinks
from annoying.functions import get_object_or_None


def clean_url(url):
    if url:
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
        val = URLValidator()
        try:
            val(url)
        except ValidationError, e:
            raise e
    return url

class ZipcodeForm(ModelForm):
    zip_code = forms.ModelChoiceField(Zipcode.objects.all(),
          widget=ChoiceWidget(
              'ZipcodeAutocomplete',
              attrs = {'placeholder':''}))
    def __init__(self, *args, **kw):
      super(ZipcodeForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        'zip_code',
      )

    class Meta:
        model = Location
        fields = ['zip_code']

class LocationForm(ModelForm):
    zip_code = forms.ModelChoiceField(Zipcode.objects.all(),
          widget=ChoiceWidget(
              'ZipcodeAutocomplete',
              attrs={'placeholder':''}))
    def __init__(self, *args, **kw):
      super(LocationForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        Div(
          Div('address_1',css_class='col-sm-6 left',),
          Div('address_2',css_class='col-sm-6 right',),
          css_class='row no-gutter',
        ),
        Div(
          Div('city',css_class='col-sm-4 left',),
          Div('state',css_class='col-sm-4 right',),
          Div('zip_code',css_class='col-sm-4 right',),
          css_class='row no-gutter',
        ),
      )

    class Meta:
        model = Location
        fields = ['address_1','address_2','city','state','zip_code',]

class NonUserLocationForm(LocationForm):

    def __init__(self, *args, **kw):
      super(NonUserLocationForm, self).__init__(*args, **kw)
      self.fields['zip_code'].required = False


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kw):
      super(ContactForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        'name',
        'email',
        'phone',
        'url',
      )

    def clean_url(self):
        return clean_url(self.cleaned_data.get("url", ""))

    class Meta:
        model = Contact
        fields = ['name','email','phone','url',]

class SocialLinksForm(forms.ModelForm):

    def __init__(self, *args, **kw):
      super(SocialLinksForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        'facebook',
        'google_plus',
        'twitter',
      )

    def clean_facebook(self):
        url = clean_url(self.cleaned_data.get("facebook", ""))
        if url and "facebook.com" not in url:
            raise ValidationError(_('Must be a Facebook URL'), code='invalid')
        return url
    def clean_google_plus(self):
        url = clean_url(self.cleaned_data.get("google_plus", ""))
        if url and "plus.google.com" not in url:
            raise ValidationError(_('Must be a Google Plus URL'), code='invalid')
        return url
    def clean_twitter(self):
        url = clean_url(self.cleaned_data.get("twitter", ""))
        if url and "twitter.com" not in url:
            raise ValidationError(_('Must be a Twitter URL'), code='invalid')
        return url

    class Meta:
        model = SocialLinks
        fields = ['facebook','google_plus','twitter',]

class PhotoLinksForm(forms.ModelForm):

    def __init__(self, *args, **kw):
      super(PhotoLinksForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        'instagram',
        'tumblr',
      )

    def clean_instagram(self):
        url = clean_url(self.cleaned_data.get("instagram", ""))
        if url and "instagram.com" not in url:
            raise ValidationError(_('Must be a Instagram URL'), code='invalid')
        return url
    def clean_tumblr(self):
        url = clean_url(self.cleaned_data.get("tumblr", ""))
        if url and "tumblr.com" not in url:
            raise ValidationError(_('Must be a Tumblr URL'), code='invalid')
        return url

    class Meta:
        model = SocialLinks
        fields = ['instagram','tumblr',]


class VideoLinksForm(forms.ModelForm):

    def __init__(self, *args, **kw):
      super(VideoLinksForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        'youtube',
        'vimeo',
      )

    def clean_youtube(self):
        url = clean_url(self.cleaned_data.get("youtube", ""))
        if url and "youtube.com" not in url:
            raise ValidationError(_('Must be a Youtube URL'), code='invalid')
        return url
    def clean_vimeo(self):
        url = clean_url(self.cleaned_data.get("vimeo", ""))
        if url and "vimeo.com" not in url:
            raise ValidationError(_('Must be a Vimeo URL'), code='invalid')
        return url

    class Meta:
        model = SocialLinks
        fields = ['youtube','vimeo',]


class MusicLinksForm(forms.ModelForm):

    def __init__(self, *args, **kw):
      super(MusicLinksForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        'bandcamp',
        'itunes',
        'spotify',
        'soundcloud',
      )

    def clean_bandcamp(self):
        url = clean_url(self.cleaned_data.get("bandcamp", ""))
        if url and "bandcamp.com" not in url:
            raise ValidationError(_('Must be a Bandcamp URL'), code='invalid')
        return url
    def clean_itunes(self):
        url = clean_url(self.cleaned_data.get("itunes", ""))
        if url and "itunes.apple.com" not in url:
            raise ValidationError(_('Must be a iTunes URL'), code='invalid')
        return url
    def clean_spotify(self):
        url = clean_url(self.cleaned_data.get("spotify", ""))
        if url and "spotify.com" not in url:
            raise ValidationError(_('Must be a Spotify URL'), code='invalid')
        return url
    def clean_soundcloud(self):
        url = clean_url(self.cleaned_data.get("soundcloud", ""))
        if url and "soundcloud.com" not in url:
            raise ValidationError(_('Must be a SoundCloud URL'), code='invalid')
        return url

    class Meta:
        model = MusicLinks
        fields = ['bandcamp','itunes','spotify','soundcloud',]
