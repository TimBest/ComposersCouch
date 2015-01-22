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
    poster = models.ForeignKey(Image, related_name='event poster',
                               null=True, blank=True)
    title = models.CharField(max_length = 255, null=True, blank=True,)
    description = models.TextField(null=True, blank=True)
    headliner_select = models.ForeignKey(MusicianProfile, null=True, blank=True,
                                  related_name='shows_headlining')
    headliner = models.CharField(max_length=255, null=True, blank=True,)
    openers_select = models.ManyToManyField(MusicianProfile, null=True, blank=True,
                                     related_name='shows_opening')
    openers = models.CharField(max_length=255, null=True, blank=True,)
    venue_select = models.ForeignKey(User, null=True, blank=True)
    venue = models.CharField(max_length=255, null=True, blank=True,)
    location = models.ForeignKey(Location, null=True, blank=True,
                                related_name='event_location')
    objects = models.GeoManager()

    def participants(self):
        participants = []
        if self.venue_select:
            participants.append(self.venue_select)
        if self.headliner_select:
            participants.append(self.headliner_select.profile.user)
        for opener in self.openers_select.all():
            participants.append(opener.profile.user)
        return participants

    def get_poster(self):
        try:
            if self.poster:
                return self.poster.image
            elif self.headliner:
                return self.headliner.profile.mugshot.image
            elif self.venue:
                return self.venue.profile.mugshot.image
        except:
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
