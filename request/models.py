from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from accounts.models import MusicianProfile
from annoying.functions import get_object_or_None
from contact.models import Zipcode
from threaded_messages.models import Thread
from schedule.models.events import DateRange


class Request(models.Model):
    accept_by = models.DateField(_("accept_by"))
    date = models.ForeignKey(DateRange, verbose_name=_("dateRange"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class PrivateRequest(Request):
    messages = models.OneToOneField(Thread, verbose_name=_("messages"),
                                   related_name='request',
                                   null=True, blank=True)
    headliner = models.ForeignKey(MusicianProfile,
                                  verbose_name=_("headliner"),
                                  related_name='request_for_headlining')
    openers = models.ManyToManyField(MusicianProfile,
                                     verbose_name=_("openers"),
                                     related_name='request_for_opening',
                                     null=True, blank=True)
    host = models.ForeignKey(User, verbose_name=_("host"), related_name='request_for_hosting',)

    def participants(self):
        participants = []
        if self.host:
            participants.append(self.host)
        if self.headliner:
            participants.append(self.headliner.profile.user)
        for opener in self.openers.all():
            participants.append(opener.profile.user)
        return participants

    def has_accepted(self, user):
        a = get_object_or_None(Accept, user=user, request=self)
        if a:
            return a.accepted
        else:
            return None

class Accept(models.Model):
    user = models.ForeignKey(User, related_name='accepter')
    request = models.ForeignKey(PrivateRequest, related_name='accepted_request')
    accepted = models.BooleanField(default=False)

class PublicRequest(Request):
    zip_code = models.ForeignKey(Zipcode, verbose_name=_("Zipcode"))
    details = models.TextField(_("description"))
    fulfilled = models.BooleanField(_('fulfilled'), default=False)
    requester = models.ForeignKey(User, verbose_name=_("requester"))
    objects = models.GeoManager()

    def save(self, requester=None, date=None, *args, **kwargs):
        if requester:
            self.requester = requester
        if date:
            self.date = date
        super(PublicRequest, self).save(*args, **kwargs)

class NumberOfApplicants(models.Model):
    public_request = models.OneToOneField(PublicRequest,
                                          verbose_name=_("public_request"),
                                          related_name='applicants',)
    left = models.PositiveSmallIntegerField(verbose_name=_("total_bands"))
    total = models.PositiveSmallIntegerField(verbose_name=_("number_of_bands"))

    def save(self, public_request=None, *args, **kwargs):
        if public_request:
            self.public_request = public_request
        if not self.left:
            self.left = self.total
        super(NumberOfApplicants, self).save(*args, **kwargs)

class Application(models.Model):
    public_request = models.ForeignKey(PublicRequest,
                                       verbose_name=_("public_request"),
                                       related_name='applications',)
    thread = models.OneToOneField(Thread, verbose_name=_("thread"),
                                   related_name='application',
                                   null=True, blank=True)
    applicant = models.ForeignKey(User, verbose_name=_("requester"))
    approved = models.NullBooleanField(_('approved'), default=None)
