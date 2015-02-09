from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from accounts.models import Profile


class FanProfile(Profile):
    profile = models.OneToOneField(Profile,
                                   unique=True,
                                   verbose_name=_('profile'),
                                   related_name='fanProfile')
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s %s' % (self.profile.user.first_name, self.profile.user.last_name)
