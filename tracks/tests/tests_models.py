from django.contrib.auth.models import User
from django.test import TestCase

from request.models import PrivateRequest, RequestParticipant


class PrivateRequestModelTest(TestCase):
    fixtures = ['users', 'profiles', 'contactInfos','locations', 'contacts',
                'zipcodes', 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates',
                'privateRequests', 'requestParticipants']

    # TODO
    def test_has_accepted(self):
        private_request = PrivateRequest.objects.get(pk=1)
        # test that invalid user returns None
        user_invalid = User.objects.get(pk=1)
        self.assertEqual(private_request.has_accepted(user_invalid), None)
        # test that a user that accepted returns true
        user_accepted = User.objects.get(pk=2)
        self.assertEqual(private_request.has_accepted(user_accepted), True)
        # test a user that hasnt responded returns None
        user_null = User.objects.get(pk=3)
        self.assertEqual(private_request.has_accepted(user_null), None)
        # test a user that denied returns false

    def test_headliner(self):
        #TODO: add this test
        pass

    def test_venue(self):
        self.assertEqual(
            PrivateRequest.objects.get(pk=1).venue(),
            RequestParticipant.objects.get(pk=2)
        )

    def test_openers(self):
        # TODO: expand to test multiple openers
        self.assertEqual(
            PrivateRequest.objects.get(pk=1).openers().first(),
            RequestParticipant.objects.get(pk=1)
        )
