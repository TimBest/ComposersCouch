from django.contrib.gis.db import models
from django.utils.translation import ugettext as _


class SocialLinks(models.Model):
    profile = models.OneToOneField('accounts.Profile', unique=True,
                                   primary_key=True,
                                   verbose_name=_('profile'),
                                   related_name='social_links')
    facebook    =  models.CharField(_("facebook"), max_length=200, blank=True)
    google_plus =  models.CharField(_("google plus"), max_length=200, blank=True)
    instagram   =  models.CharField(_("instagram"), max_length=200, blank=True)
    tumblr      =  models.CharField(_("tumblr"), max_length=200, blank=True)
    twitter     =  models.CharField(_("twitter"), max_length=200, blank=True)
    youtube     =  models.CharField(_("youtube"), max_length=200, blank=True)
    vimeo       =  models.CharField(_("vimeo"), max_length=200, blank=True)

class MusicLinks(models.Model):
    profile = models.OneToOneField('artist.ArtistProfile', unique=True,
                                   null=True, blank=True,
                                   verbose_name=_('profile'),
                                   related_name='music_links')
    bandcamp =  models.CharField(_("bandcamp"), max_length=200, blank=True)
    itunes =  models.CharField(_("itunes"), max_length=200, blank=True)
    spotify =  models.CharField(_("spotify"), max_length=200, blank=True)
    soundcloud =  models.CharField(_("soundcloud"), max_length=200, blank=True)
