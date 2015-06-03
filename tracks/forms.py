import mutagen
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelMultipleChoiceField, Textarea
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm
from multiupload.fields import MultiFileField

from annoying.functions import get_object_or_None
from artist.models import ArtistProfile
from social_links.forms import clean_url
from embed_video.fields import EmbedVideoFormField
from tracks.models import Album, Track, Media


class TracksForm(ModelForm):
    tracks = MultiFileField(required=False, max_num=15, min_num=0,
                            max_file_size=settings.MAX_AUDIO_UPLOAD_SIZE,
                            help_text="Currently supports .mp3 and .ogg",)

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
                        username=self.instance.artist_profile.profile.user.username,
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
        self.fields['tracks'].help_text = "Currently supports .mp3 and .ogg"

    class Meta:
        model = Album
        widgets = {
            'description' : Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ['title', 'year', 'genre', 'description']

class AlbumAudioForm(ModelForm):
    title = forms.CharField(max_length=128)
    audio = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(AlbumAudioForm, self).__init__(*args, **kwargs)
        track = kwargs.get('instance', None)
        if track:
            self.fields['title'].initial = track.media.title

    def save(self, commit=False):
        remove = self.cleaned_data.get('DELETE', False)
        formData = super(AlbumAudioForm, self).save(commit=False)
        if remove:
            track = get_object_or_None(Track, id=formData.id)
            if track:
                track.media.delete()
                track.delete()
            return None
        return formData

    class Meta:
        model = Track
        fields = ['album','order','id']

class AlbumVideoForm(ModelForm):
    video = EmbedVideoFormField(required=False)
    title = forms.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(AlbumVideoForm, self).__init__(*args, **kwargs)
        track = kwargs.get('instance', None)
        if hasattr(track, 'media'):
            self.fields['title'].initial = track.media.title
            self.fields['video'].initial = track.media.video

    class Meta:
        model = Track
        fields = ['album','order']

    def clean_video(self):
        url = clean_url(self.cleaned_data.get("video", ""))
        if "youtube.com" in url or "vimeo.com" in url:
            return url
        elif url:
            raise ValidationError(_('Must be a Youtube or Vimeo URL.'), code='invalid')

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
