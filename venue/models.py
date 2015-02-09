from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from accounts.models import Profile
from contact.models import Contact
from photos.models import Image


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

WEEKDAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday',]

class Hours(models.Model):
    profile = models.ForeignKey(VenueProfile,
                                verbose_name=_("venue"),
                                related_name="hours")
    weekday = models.CharField(_("weekday"), max_length=1,
                               help_text=_("0-6 (0=Monday)"))
    start = models.TimeField(_("start"), null=True, blank=True)
    end = models.TimeField(_("end"), null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(WEEKDAYS[int(self.weekday)])

CATEGORY_CHOICES = (
    ('Sound', _('Sound')),
    ('Effects', _('Effects')),
    ('Accessories', _('Accessories')),
)
QUANTITY_CHOICES = (
    ('1', _('1')),
    ('2', _('2')),
    ('3', _('3')),
    ('4', _('4')),
    ('5', _('5')),
    ('6', _('6')),
    ('7', _('7')),
    ('8', _('8')),
    ('9', _('9')),
)
class Equipment(models.Model):
    profile = models.ForeignKey(VenueProfile,
                                verbose_name=_("venue"),
                                related_name="equipment")
    name =  models.CharField(_("name"), max_length=64, null=True, blank=True)
    quantity =  models.CharField(_("quantity"), max_length=1,
                                 choices=QUANTITY_CHOICES,
                                 default="",
                                 null=True, blank=True)
    category =  models.CharField(_('category'), max_length=11,
                                 choices=CATEGORY_CHOICES,
                                 default="",
                                 null=True, blank=True)
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Seating(models.Model):
    profile = models.OneToOneField(VenueProfile,
                                   verbose_name=_("venue"),
                                   related_name="seating")
    capacity =  models.CharField(_("capacity"), max_length=6, null=True, blank=True)
    seating_chart = models.ForeignKey(Image, verbose_name=_("seating chart"),null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.capacity)

class Policies(models.Model):
    profile = models.ForeignKey(VenueProfile,
                                verbose_name=_("venue"),
                                related_name="policies")
    title =  models.CharField(_("title"), max_length=64, null=True, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.title)

class Staff(models.Model):
    profile = models.ForeignKey(VenueProfile,
                                verbose_name=_("venue"),
                                related_name="staff")
    contact = models.ForeignKey(Contact, verbose_name=_("contact"), null=True, blank=True)
    job_title =  models.CharField(_("job title"), max_length=64, null=True, blank=True)
    biography = models.TextField(_("biography"), null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.job_title)
