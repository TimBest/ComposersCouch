from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from sorl.thumbnail import ImageField

from contact.models import ContactInfo
from genres.models import Genre
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
                                   related_name='genre_artist',
                                   null=True, blank=True)
    contact_info = models.OneToOneField(ContactInfo, unique=True,
                                        blank=True, null=True,
                                        verbose_name=_('contactInfo'),
                                        related_name='contactInfo')
    has_owner = models.BooleanField(default=True)
    profile_type = models.CharField(_('profile type'),
                                     max_length=1,
                                     choices=PROFILE_TYPE_CHOICES,
                                     default=PROFILE_TYPE_CHOICES[1][0])
    objects = models.GeoManager()

    def __unicode__(self):
        profileType = self.profile_type
        if profileType == 'f':
            return u'%s %s' % (self.user.first_name, self.user.last_name)
        elif profileType == 'm':
            return '%s' % self.artist_profile.name
        elif profileType == 'v':
            return '%s' % self.venueProfile.name
        return '%s' % self.user.username

    def get_absolute_url(self):
        profileType = self.profile_type
        if profileType == 'f':
            return ('fan:home', [self.user.username])
        elif profileType == 'm':
            return ('artist:home', [self.user.username])
        elif profileType == 'v':
            return ('venue:home', [self.user.username])
        return ('home')

    get_absolute_url = models.permalink(get_absolute_url)
