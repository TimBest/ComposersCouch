from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from annoying.functions import get_object_or_None
from contact.models import Zipcode
from threads.models import Thread, Participant
from schedule.models.events import DateRange


class Request(models.Model):
    date = models.ForeignKey(DateRange, verbose_name=_("dateRange"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

""" Private Request """
ROLE_CHOICES = (
    ('h', _('Headliner')),
    ('o', _('Openers')),
    ('v', _('Venue')),
)
class PrivateRequest(Request):
    thread = models.OneToOneField(Thread, verbose_name=_("thread"),
                                   related_name='request',
                                   null=True, blank=True)

    def has_accepted(self, user):
        participant = get_object_or_None(Participant, user=user, thread=self.thread)
        if participant:
            return participant.request_participant.first().accepted
        else:
            return None

    def headliner(self):
        return get_object_or_None(RequestParticipant, participant__thread=self.thread, role='h')

    def venue(self):
        return RequestParticipant.objects.get(participant__thread=self.thread, role='v')

    def openers(self):
        return RequestParticipant.objects.filter(participant__thread=self.thread, role='o')

class RequestParticipant(models.Model):
    participant = models.ForeignKey(Participant, related_name='request_participant')
    role =  models.CharField(_('role'), max_length=1, choices=ROLE_CHOICES)
    accepted = models.NullBooleanField(_('approved'), default=None)

""" Public Request """
class PublicRequest(Request):
    accept_by = models.DateField(_("accept_by"), null=True, blank=True)
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
    public_request = models.OneToOneField(PublicRequest, primary_key=True,
                                          verbose_name=_("public_request"),
                                          related_name='applicants',)
    left = models.PositiveSmallIntegerField(verbose_name=_("total bands"))
    total = models.PositiveSmallIntegerField(verbose_name=_("number of bands"))

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
