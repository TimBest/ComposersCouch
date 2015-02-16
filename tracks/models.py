import os
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from .utils import json_playlist
from audiofield.fields import AudioField
from embed_video.fields import EmbedVideoField
from genres.models import Genre
from photos.models import Image


def get_audio_upload_path(instance, filename):
    if hasattr(instance, 'upload_to_info'):
        username, track_type, album_title = instance.upload_to_info
        if album_title:
            return os.path.join(username, track_type, album_title, filename)
        else:
            return os.path.join(username, track_type, filename)
    else:
        return os.path.join(instance.title, filename)

class Album(models.Model):
    artist_profile = models.ForeignKey('artist.ArtistProfile',
                          related_name='albums',null=True,
                          blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    album_art = models.ForeignKey(Image,
                          related_name='artist Album art',null=True,
                          blank=True)
    title = models.CharField(_('Title'), max_length=100)
    genre = models.ManyToManyField(Genre, verbose_name=_("genre"),
                                   related_name='album_genre',
                                   null=True, blank=True)
    year = models.CharField(_("Year"), max_length="4", null=True,
                            blank=True)
    description = models.TextField(_("Description"), null=True,
                                   blank=True)

    def __unicode__(self):
        return '%s'% self.id

    def get_json_playlist(self):
        if not hasattr(self, '_cached_playlist'):
            self._cached_playlist = json_playlist(self.track_set.all(), self)
        return self._cached_playlist

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp3','.oga']
    if not ext in valid_extensions:
        raise ValidationError(u'File type not supported')

class Media(models.Model):
    title = models.CharField(_('Title'), max_length=128)
    video = EmbedVideoField(_('Video Link'), null=True, blank=True,
                            help_text="Link to youtube or vimeo")
    audio = AudioField(_("Audio file"), upload_to=get_audio_upload_path,
                       ext_whitelist=('.mp3','.ogg'),
                       help_text="Currently supports mp3 and ogg",
                       null=True, blank=True)
    live = models.BooleanField(default=False)

    def set_upload_to_info(self, username, track_type, album_title=None):
        """
            username = username of who saving the model
            track_type = albums/covers/interviews
            album_title = if album whats its title
        """
        self.upload_to_info = (username, track_type, album_title)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='track_set')
    order = models.PositiveSmallIntegerField(verbose_name=_("order"))
    media = models.OneToOneField(Media, related_name='album_track')

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return '%s'% self.id
