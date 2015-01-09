from django import forms
from django.forms import ModelChoiceField, ModelMultipleChoiceField, Textarea
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Layout

from accounts.models import Genre, MusicianProfile
from embed_video.fields import EmbedVideoFormField
from tracks.models import Album, Cover, Track, Media, Interview


class AlbumForm(ModelForm):

    def __init__(self, *args, **kw):
        super(AlbumForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
          Div(
            Div('title',css_class='col-sm-6 left',),
            Div('year',css_class='col-sm-6 right',),
            css_class='row no-gutter',
          ),
          'genre',
          'description',
          HTML("<label>Tracks</label><input type='file' name='tracks' multiple>")
        )

    class Meta:
        model = Album
        widgets = {
            'description' : Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ['title', 'genre', 'year', 'description']


class AlbumAudioForm(ModelForm):
    title = forms.CharField(max_length=128)
    audio = forms.FileField(required=False)
    def __init__(self, *args, **kwargs):
        super(AlbumAudioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div('album',css_class='hidden',),
                    Div(
                    Div('order',css_class='col-xs-2 left',),
                    Div('title',css_class='col-xs-9 center',),
                    Div(HTML("<label>Remove</label>{{ form.DELETE }}"),css_class='col-xs-1 right',),
                    css_class='row no-gutter',
                ),
                Div(
                  HTML (
                    "<label>Currently</label><audio controls><source src='{{media_url}}{{track.media.audio}}' type='audio/mp3'>Your browser does not support the audio element.</audio>"
                  ),
                  css_class='audio-layout row no-gutter',
                ),
              css_class='track-formset',
            ),
        )
        track = kwargs.get('instance', None)
        if track:
            self.fields['title'].initial = track.media.title

    class Meta:
        model = Track
        fields = ['album','order',]

class AlbumVideoForm(ModelForm):
    video = EmbedVideoFormField(required=False)
    title = forms.CharField(max_length=128)
    def __init__(self, *args, **kwargs):
        super(AlbumVideoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div('album',css_class='hidden',),
                Div(
                  Div('order',css_class='col-xs-2 left',),
                  Div('title',css_class='col-xs-5 left',),
                  Div('video',css_class='col-xs-5 right',),
                  css_class='row no-gutter',
                ),
                css_class='track-formset',
            ),
        )
        track = kwargs.get('instance', None)
        if track:
            self.fields['title'].initial = track.media.title

    class Meta:
        model = Track
        fields = ['album','order']


"""
video_layout = Layout(
  Div(
    Div('title',css_class='col-xs-6 left',),
    Div('video',css_class='col-xs-6 right',),
    css_class='row no-gutter',
  ),
)

audio_layout = Layout(
  Div(
    Div(
      HTML (
        "<label>Currently</label><audio controls><source src='{{media_url}}{{track.media.audio}}' type='audio/mp3'>Your browser does not support the audio element.</audio>"
      ),
      css_class='col-sm-6 left',
    ),
    Div(
      'audio',
      css_class='col-sm-6 right',
    ),
    css_class='audio-layout row no-gutter',
  ),
)
class AudioForm(ModelForm):
    def __init__(self, *args, **kw):
        super(AudioForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'title',
                'live',
                audio_layout,
                css_class='track-formset',
            ),
        )

    class Meta:
        model = Media
        fields = ['audio','live','title',]

class VideoForm(ModelForm):

    def __init__(self, *args, **kw):
        super(AlbumTrackForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'title',
                'live',
                'video',
                css_class='track-formset',
            ),
        )

    class Meta:
        model = Media
        fields = ['video','live','title',]



class TrackForm(ModelForm):

    def __init__(self, *args, **kw):
        super(TrackForm, self).__init__(*args, **kw)
        self.fields['host'].required = False
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'title',
                'host',
            ),
        )

    class Meta:
        model = LiveTrack
        fields = ['title', 'host']

class HostTrackForm(ModelForm):

    def __init__(self, *args, **kw):
        super(HostTrackForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'title',
                'musician',
            ),
        )

    class Meta:
        model = LiveTrack
        fields = ['title', 'musician']"""
