from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase
from django.test.client import RequestFactory

from accounts.models import Profile
from customProfile.decorators import is_venue, is_artist, is_fan


class IsVenueDecoratorTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',]

    def setUp(self):
        # create mock function and decorate it
        func = lambda x: x
        self.decorated_func = is_venue(func)
        factory = RequestFactory()
        self.request = factory.get(reverse('home'))
        # create user
        self.user = User.objects.get(pk=1)
        self.user.profile = Profile.objects.get(pk=1)
        self.user.profile.save()

    def test_anonymous_user(self):
        self.request.user = auth.get_user(self.client)
        response = self.decorated_func(self.request)
        self.assertEqual(response.status_code, 302)

    def test_fan(self):
        user = self.user
        user.profile.profile_type = 'f'
        user.profile.save()
        self.request.user = user
        self.assertRaises(PermissionDenied, self.decorated_func, self.request)

    def test_artist(self):
        user = self.user
        user.profile.profile_type = 'm'
        user.profile.save()
        self.request.user = user
        self.assertRaises(PermissionDenied, self.decorated_func, self.request)

    def test_venue(self):
        user = self.user
        user.profile.profile_type = 'v'
        user.profile.save()
        self.request.user = user
        response = self.decorated_func(self.request)
        self.assertIsInstance(response, WSGIRequest)

class IsArtistDecoratorTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',]

    def setUp(self):
        # create mock function and decorate it
        func = lambda x: x
        self.decorated_func = is_artist(func)
        factory = RequestFactory()
        self.request = factory.get(reverse('home'))
        # create user
        self.user = User.objects.get(pk=1)
        self.user.profile = Profile.objects.get(pk=1)
        self.user.profile.save()

    def test_anonymous_user(self):
        self.request.user = auth.get_user(self.client)
        response = self.decorated_func(self.request)
        self.assertEqual(response.status_code, 302)

    def test_fan(self):
        user = self.user
        user.profile.profile_type = 'f'
        user.profile.save()
        self.request.user = user
        self.assertRaises(PermissionDenied, self.decorated_func, self.request)

    def test_artist(self):
        user = self.user
        user.profile.profile_type = 'm'
        user.profile.save()
        self.request.user = user
        response = self.decorated_func(self.request)
        self.assertIsInstance(response, WSGIRequest)

    def test_venue(self):
        user = self.user
        user.profile.profile_type = 'v'
        user.profile.save()
        self.request.user = user
        self.assertRaises(PermissionDenied, self.decorated_func, self.request)

class IsFanDecoratorTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',]

    def setUp(self):
        # create mock function and decorate it
        func = lambda x: x
        self.decorated_func = is_fan(func)
        factory = RequestFactory()
        self.request = factory.get(reverse('home'))
        # create user
        self.user = User.objects.get(pk=1)
        self.user.profile = Profile.objects.get(pk=1)
        self.user.profile.save()

    def test_anonymous_user(self):
        self.request.user = auth.get_user(self.client)
        response = self.decorated_func(self.request)
        self.assertEqual(response.status_code, 302)

    def test_fan(self):
        user = self.user
        user.profile.profile_type = 'f'
        user.profile.save()
        self.request.user = user
        response = self.decorated_func(self.request)
        self.assertIsInstance(response, WSGIRequest)

    def test_artist(self):
        user = self.user
        user.profile.profile_type = 'm'
        user.profile.save()
        self.request.user = user
        self.assertRaises(PermissionDenied, self.decorated_func, self.request)

    def test_venue(self):
        user = self.user
        user.profile.profile_type = 'v'
        user.profile.save()
        self.request.user = user
        self.assertRaises(PermissionDenied, self.decorated_func, self.request)
