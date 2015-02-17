import datetime
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
import pytz

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from contact.models import Location
from schedule.models import Event, Calendar, Show


class TestEvent(TestCase):

    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',  
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']

    def test_get_absolute_url(self):
        event = Event.objects.get(pk=3)
        event.get_absolute_url()

    def test_get_loaction(self):
        # if info has a location return it
        event = Event.objects.get(pk=3)
        location = Location.objects.get(pk=1)
        event.show.info.location = location
        event.show.info.save()
        self.assertEqual(event.get_location(),location)
        # if there is no location return the venues loaction
        event.show.info.location = None
        event.show.info.save()
        user = User.objects.get(pk=3)
        self.assertEqual(event.get_location(),user.profile.contact_info.location)
        # if there is no show location and no venue location return the users loaction
        event.show.info.venue = None
        event.show.info.save()
        self.assertEqual(event.get_location(),event.calendar.owner.profile.contact_info.location)

class TestShow(TestCase):

    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']


    def test_update_visible_and_approved(self):
        show = Show.objects.get(pk=3)
        event_1 = Event.objects.get(pk=3)
        event_2 = Event.objects.get(pk=4)
        # all events approved and visible
        event_1.approved = True
        event_1.visible = True
        event_1.save()
        event_2.approved = True
        event_2.visible = True
        event_2.save()
        show.save()
        self.assertTrue(show.approved)
        self.assertTrue(show.visible)
        # one event non approved
        event_1.approved = False
        event_1.visible = True
        event_1.save()
        event_2.approved = True
        event_2.visible = True
        event_2.save()
        show.save()
        self.assertFalse(show.approved)
        self.assertFalse(show.visible)
        # all events are not approved and not visible
        event_1.approved = False
        event_1.visible = False
        event_1.save()
        event_2.approved = False
        event_2.visible = False
        event_2.save()
        show.save()
        #both events are approved but only one is visible
        self.assertFalse(show.approved)
        self.assertFalse(show.visible)
        event_1.approved = True
        event_1.visible = True
        event_1.save()
        event_2.approved = True
        event_2.visible = False
        event_2.save()
        show.save()
        self.assertTrue(show.approved)
        self.assertTrue(show.visible)
        # both events are aproved but not visible
        event_1.approved = True
        event_1.visible = False
        event_1.save()
        event_2.approved = True
        event_2.visible = False
        event_2.save()
        show.save()
        self.assertTrue(show.approved)
        self.assertFalse(show.visible)
