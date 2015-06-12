from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from artist.models import ArtistProfile
from contact.models import Location
from object_or_text.fields import ObjectOrTextField
from object_or_text.model_fields import ObjectOrTextField as ObjectOrTextFieldTemp
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
    poster = models.ForeignKey(Image, related_name='event_poster',
                               null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length = 255, null=True, blank=True,)
    description = models.TextField(null=True, blank=True)
    headliner = ObjectOrTextField(ArtistProfile,
                                  verbose_name=_("headliner"),
                                  related_name='shows_headlining',
                                  null=True, blank=True, max_length=255)
    #headliner_temp = ObjectOrTextFieldTemp(blank=True, null=True,
    #                                       verbose_name=_("headliner_temp"), max_length=255)
    openers = models.ManyToManyField(ArtistProfile, blank=True,
                                     related_name='shows_opening')
    openers_text = models.CharField(max_length=255, null=True, blank=True,)
    venue = ObjectOrTextField(User, verbose_name=_("venue"),
                              related_name='shows_hosting',
                              null=True, blank=True, max_length=255)
    #venue_temp = ObjectOrTextFieldTemp(verbose_name=_("venue_temp"), default="No Venue Listed", max_length=255)
    location = models.ForeignKey(Location, null=True, blank=True,
                                related_name='event_location')
    objects = models.GeoManager()

    def participants(self):
        participants = []
        if self.venue:
            participants.append(self.venue)
        if self.headliner:
            participants.append(self.headliner.profile.user)
        for opener in self.openers.all():
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
