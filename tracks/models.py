import mutagen, os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from sorl.thumbnail import ImageField

from .utils import json_playlist
from embed_video.fields import EmbedVideoField
from photos.models import Image


class Genre(models.Model):
    name =  models.CharField(_("name"), max_length=64)
    slug =  models.CharField(_("slug"), max_length=64)
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Category(models.Model):
    name =  models.CharField(_("name"), max_length=64)
    slug =  models.CharField(_("slug"), max_length=64)
    genres = models.ManyToManyField(Genre, verbose_name=_("genres"),
                               related_name='categories')
    def __unicode__(self):
        return u'{0}'.format(self.name)

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
    musician_profile = models.ForeignKey('accounts.MusicianProfile',
                          verbose_name=_("musician profile"),
                          related_name='albums',null=True,
                          blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    album_art = models.ForeignKey(Image,
                          verbose_name=_("Album art"),
                          related_name='musician Album art',null=True,
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
    valid_extensions = ['.mp3','.ogv','.m4v','.oga']
    if not ext in valid_extensions:
        raise ValidationError(u'File type not supported')

class Media(models.Model):
    title = models.CharField(_('Title'), max_length=128)
    video = EmbedVideoField(verbose_name = _('video'),null=True, blank=True, help_text="Link to youtube or vimeo")
    audio = models.FileField(_("Audio file"), upload_to=get_audio_upload_path, validators=[validate_file_extension], null=True, blank=True)
    live = models.BooleanField(default=False)

    def save(self, audio=None, *args, **kwargs):
        if audio:
            file = self.audio.open()
            file_path = file.temporary_file_path()
            metadata = mutagen.File(file_path, easy=True)
            if metadata and metadata.get('title'):
                     title=metadata.get('title')[0]
            if not self.title:
                pass
        super(Media, self).save(*args, **kwargs)

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

#class Cover(models.Model):
#    media = models.OneToOneField(Media, verbose_name=_("media"),null=True, blank=True)
#    musician = models.ForeignKey('accounts.MusicianProfile', related_name='covers')
#    target_musician = models.ForeignKey('accounts.MusicianProfile', related_name='ceverd')

#class Interview(models.Model):
#    media = models.OneToOneField(Media, verbose_name=_("media"),null=True, blank=True)
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)
#    musician = models.ForeignKey('accounts.MusicianProfile', verbose_name=_("musician profile"), related_name='interviews')
#    host = models.ForeignKey(User, verbose_name=_("host profile"), related_name='interviews_hosted', null=True, blank=True)
