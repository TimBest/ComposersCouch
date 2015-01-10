import mutagen
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelMultipleChoiceField, Textarea
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Layout
from multiupload.fields import MultiFileField

from accounts.models import MusicianProfile
from embed_video.fields import EmbedVideoFormField
from tracks.models import Album, Track, Media


class TracksForm(ModelForm):
    tracks = MultiFileField(required=False, max_num=15, min_num=0, max_file_size=settings.MAX_AUDIO_UPLOAD_SIZE)
    def __init__(self, *args, **kw):
        super(TracksForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
          'tracks',
        )

    class Meta:
        model = Album
        fields = []

    def save(self, request, commit=True):
        super(TracksForm, self).save(commit=commit)
        if commit:
            tracks_on_album = Track.objects.filter(album=self.instance).count() + 1
            for file in self.cleaned_data['tracks']:
                try:
                    file_path = file.temporary_file_path()
                    metadata = mutagen.File(file_path, easy=True)
                    if metadata and metadata.get('title'):
                        title=metadata.get('title')[0]
                except:
                    title = ""
                media = Media(audio=file, title=title)
                try:
                    media.full_clean()
                    media.set_upload_to_info(
                        username=self.instance.musician_profile.profile.user.username,
                        track_type="albums",
                        album_title=self.instance.title
                    )
                    media.save()
                    track = Track(media=media, order=tracks_on_album, album=self.instance)
                    tracks_on_album += 1
                    track.save()
                except ValidationError as e:
                    messages.error(request, e.messages[0]+" : "+str(file))
        return self.instance

class AlbumForm(TracksForm):

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
          'tracks',
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
        if hasattr(track, 'media'):
            self.fields['title'].initial = track.media.title
            self.fields['video'].initial = track.media.video

    class Meta:
        model = Track
        fields = ['album','order']

    def save(self, commit):
        track = super(AlbumVideoForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        video = self.cleaned_data.get('video')
        if hasattr(track, 'media'):
            track.media.title = title
            track.media.video = video
            track.media.save()
        else:
            media = Media(title=title, video=video)
            media.save()
            track.media = media
            track.save()
        return track
