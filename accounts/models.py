from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from sorl.thumbnail import ImageField

from contact.models import ContactInfo
from tracks.models import Genre
from userena.models import UserenaBaseProfile


PROFILE_TYPE_CHOICES = (
    ('f', _('Fan')),
    ('m', _('Musician')),
    ('v', _('Venue')),
)

class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    genre = models.ManyToManyField(Genre, verbose_name=_("genre"),
                                   related_name='genre_musician',
                                   null=True, blank=True)
    contact_info = models.OneToOneField(ContactInfo, unique=True,
                                        blank=True, null=True,
                                        verbose_name=_('contactInfo'),
                                        related_name='contactInfo')
    has_owner =  models.BooleanField(default=True)
    profile_type =  models.CharField(_('profile type'),
                                     max_length=1,
                                     choices=PROFILE_TYPE_CHOICES,
                                     default=PROFILE_TYPE_CHOICES[1][0])
    objects = models.GeoManager()

    def __unicode__(self):
        profileType = self.profile_type
        if profileType == 'f':
            return u'%s %s' % (self.user.first_name, self.user.last_name)
        elif profileType == 'm':
            return '%s' % self.musicianProfile.name
        elif profileType == 'v':
            return '%s' % self.venueProfile.name
        return '%s' % self.user.username

class FanProfile(Profile):
    profile = models.OneToOneField(Profile,
                                   unique=True,
                                   verbose_name=_('profile'),
                                   related_name='fanProfile')
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s %s' % (self.profile.user.first_name, self.profile.user.last_name)

class MusicianProfile(Profile):
    profile = models.OneToOneField(Profile,
                                   unique=True,
                                   verbose_name=_('profile'),
                                   related_name='musicianProfile')
    name =  models.CharField(_('band name'), max_length=64,
                                  blank=False)
    biography = models.TextField(_("biography"), null=True, blank=True)
    booking_contact = models.ForeignKey(ContactInfo,
                                unique=True, null=True, blank=True,
                                verbose_name=_('bookingContact'),
                                related_name='bookingContact')
    label_contact = models.ForeignKey(ContactInfo,
                                unique=True, null=True, blank=True,
                                verbose_name=_('labelContact'),
                                related_name='labelContact')
    management_contact = models.ForeignKey(ContactInfo,
                                unique=True, null=True, blank=True,
                                verbose_name=_('managementContact'),
                                related_name='managementContact')
    press_contact = models.ForeignKey(ContactInfo,
                                unique=True, null=True, blank=True,
                                verbose_name=_('pressContact'),
                                related_name='pressContact')
    objects = models.GeoManager()

    def __unicode__(self):
        return '%s' % self.name

class VenueProfile(Profile):
    profile = models.OneToOneField(Profile, unique=True,
                          verbose_name=_('profile'),
                                related_name='venueProfile')
    name =  models.CharField(_('venue name'), max_length=64,
                                   blank=False)
    biography = models.TextField(_("biography"), null=True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return '%s' % self.name
