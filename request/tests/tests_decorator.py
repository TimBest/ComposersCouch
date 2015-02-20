from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from accounts.models import Profile
from request.decorators import is_participant

@is_participant
def mock_fn(request, *args, **kwargs):
    return request

class IsParticipantDecoratorTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',
                'profiles', 'threads', 'messages', 'participants',
                'privateRequests', 'dates']

    def setUp(self):
        # create WSGIRequest object
        factory = RequestFactory()
        self.request = factory.get(reverse('home'))

    def test_anonymous_user(self):
        self.request.user = auth.get_user(self.client)
        response = mock_fn(self.request, request_id=1)
        self.assertEqual(response.status_code, 302)

    def test_non_participant(self):
        user = User.objects.get(pk=1)
        user.profile = Profile.objects.get(pk=1)
        user.profile.save()
        self.request.user = user
        self.assertRaises(PermissionDenied, mock_fn, self.request, request_id=1)

    def test_participant(self):
        for pk in [2,3]:
            user = User.objects.get(pk=2)
            user.profile = Profile.objects.get(pk=2)
            user.profile.save()
            self.request.user = user
            response = mock_fn(self.request, request_id=1)
            self.assertEqual(response, self.request)
