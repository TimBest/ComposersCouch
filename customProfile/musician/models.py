from django.db import models
from django.utils.translation import ugettext as _

from accounts.models import MusicianProfile


class Instrument(models.Model):
    name =  models.CharField(_("name"), max_length=64)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Member(models.Model):
    musician_profile = models.ForeignKey(MusicianProfile, verbose_name=_("musician profile"), related_name='members', null=True, blank=True)
    name =  models.CharField(_("name"), max_length=64)
    current_member =  models.BooleanField(_("is current member"), default=True)
    instruments = models.ManyToManyField(Instrument, verbose_name=_("instrument"),
                                related_name='instrument', null=True, blank=True)
    biography = models.TextField(_("biography"), null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)
