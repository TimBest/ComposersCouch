from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

from accounts.models import MusicianProfile
from contact.models import Location
from photos.models import Image


AGE = (
    ('All', _('All')),
    ('18+', _('18+')),
    ('21+', _('21+')),
)
class Info(models.Model):
    '''
    This model stores meta data for a date.  You can relate this data to many
    other models.
    '''
    poster = models.ForeignKey(Image,
                              verbose_name=_("Poster"),
                              related_name='event poster',null=True,
                              blank=True)
    title = models.CharField(_("title"), max_length = 255, null=True, blank=True,)
    description = models.TextField(_("description"), null=True,
                                   blank=True)
    headliner = models.ForeignKey(MusicianProfile,
                                  null=True, blank=True,
                                  verbose_name=_("headliner"),
                                  related_name='shows_headlining')
    openers = models.ManyToManyField(MusicianProfile,
                                     null=True, blank=True,
                                     verbose_name=_("openers"),
                                     related_name='shows_opening')
    host = models.ForeignKey(User, verbose_name=_("host"))
    location = models.ForeignKey(Location,
                                null=True, blank=True,
                                verbose_name=_("location"),
                                related_name='event_location')
    age =  models.CharField(_('age'), max_length=3, choices=AGE,
                            default=AGE[0][0])
    advance_price = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=True, blank=True,
                                        verbose_name=_("advance_price"))
    full_price = models.DecimalField(max_digits=6, decimal_places=2,
                                     null=True, blank=True,
                                     verbose_name=_("full_price"))
    objects = models.GeoManager()

    def participants(self):
        participants = []
        if self.host:
            participants.append(self.host)
        if self.headliner:
            participants.append(self.headliner.profile.user)
        for opener in self.openers.all():
            participants.append(opener.profile.user)
        return participants

    def get_poster(self):
        if self.poster:
            return self.poster.image
        elif self.headliner:
            return self.headliner.profile.mugshot.image
        elif self.host:
            return self.host.profile.mugshot.image
        return None

    def get_title(self):
        if self.title:
            return self.title
        elif self.headliner:
            return self.headliner.profile
        return "Show"

    class Meta:
        verbose_name = _('info')
        app_label = 'schedule'
