from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from contact import states


class Zipcode(models.Model):
    country = models.CharField(_("country"), max_length=2)
    code = models.CharField(_("zipcode"), max_length=5, primary_key=True)
    point = models.PointField(null=False, blank=False, srid=4326, verbose_name="point")
    objects = models.GeoManager()

    def __unicode__(self):
        return _('%s') % (self.code)


class Location(models.Model):
    address_1 = models.CharField(_("address"), max_length=128, blank=True)
    address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True)
    zip_code = models.ForeignKey(Zipcode, verbose_name=_("zipcode"), null=True, blank=True)
    city = models.CharField(_("city"), max_length=64, blank=True)
    state = models.CharField(_("state"), max_length=2, blank=True,
                             choices=states.STATE_CHOICES)
    objects = models.GeoManager()

    def __unicode__(self):
        return _('%s %s %s %s') % (self.address_1, self.address_2, self.city, self.zip_code)


class Contact(models.Model):
    name =  models.CharField(_("name"), max_length=64)
    phone = models.CharField(_("phone"), max_length=10, blank=True)
    email = models.EmailField(_("email"), blank=True)
    url =  models.CharField(_("website"), max_length=200, blank=True)

    def __unicode__(self):
        return _('%s') % (self.name)

class SocialLinks(models.Model):
    profile = models.OneToOneField('accounts.Profile', unique=True,
                                   null=True, blank=True,
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
    profile = models.OneToOneField('accounts.MusicianProfile', unique=True,
                                   null=True, blank=True,
                                   verbose_name=_('profile'),
                                   related_name='music_links')
    bandcamp =  models.CharField(_("bandcamp"), max_length=200, blank=True)
    itunes =  models.CharField(_("itunes"), max_length=200, blank=True)
    spotify =  models.CharField(_("spotify"), max_length=200, blank=True)
    soundcloud =  models.CharField(_("soundcloud"), max_length=200, blank=True)


class ContactInfo(models.Model):
    location = models.OneToOneField(Location,
                                    verbose_name=_("location"),
                                    related_name='contact_info',
                                    null=True, blank=True)
    contact = models.OneToOneField(Contact,
                                   verbose_name=_("contact"),
                                   related_name='contact_info',
                                   null=True, blank=True)

    objects = models.GeoManager()
