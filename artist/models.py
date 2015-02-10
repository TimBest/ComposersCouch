from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from accounts.models import Profile
from contact.models import ContactInfo


class ArtistProfile(Profile):
    profile = models.OneToOneField(Profile,
                                   unique=True,
                                   verbose_name=_('profile'),
                                   related_name='artist_profile')
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

class Instrument(models.Model):
    name =  models.CharField(_("name"), max_length=64)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Member(models.Model):
    profile = models.ForeignKey(ArtistProfile, verbose_name=_("artist"), related_name='members', null=True, blank=True)
    name =  models.CharField(_("name"), max_length=64)
    current_member =  models.BooleanField(_("is current member"), default=True)
    instruments = models.ManyToManyField(Instrument, verbose_name=_("instrument"),
                                related_name='instrument', null=True, blank=True)
    biography = models.TextField(_("biography"), null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)