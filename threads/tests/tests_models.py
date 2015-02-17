from django.contrib.auth.models import User
from django.test import TestCase

from threads import models


class PrivateRequestModelTest(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',  
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates',
                'privateRequests', 'requestParticipants']

    def test_inbox(self):
        pass

    def test_outbox(self):
        pass

    def test_trash(self):
        pass

    def test_get_absolute_url(self):
        # request
        # show
        # application
        # message
        pass

    def test_new(self):
        pass

    def test_replied(self):
        pass

    def test_last_other_sender(self):
        pass

    def test_last_others(self):
        pass

    def test_get_next(self):
        pass

    def test_get_prev(self):
        pass

    def test_read_thread(self):
        pass

    def test_cached_inbox_count_for(self):
        pass

    def test_inbox_count_for(self):
        pass
