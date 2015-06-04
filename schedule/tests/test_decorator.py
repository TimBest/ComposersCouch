from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from accounts.models import Profile
from schedule.decorators import edit_show, view_show
from schedule.models import Event, Show


@edit_show
def mock_fn(request, *args, **kwargs):
    return request

class editShowDecoratorTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'calendars', 'info',
                'shows', 'events']

    def setUp(self):
        # create WSGIRequest object
        factory = RequestFactory()
        self.request = factory.get(reverse('home'))

    def test_anonymous_user(self):
        self.request.user = auth.get_user(self.client)
        response = mock_fn(self.request, request_id=1)
        self.assertEqual(response.status_code, 302)

    def test_user_without_event(self):
        user = User.objects.get(pk=1)
        user.profile = Profile.objects.get(pk=1)
        user.profile.save()
        self.request.user = user
        self.assertRaises(PermissionDenied, mock_fn, self.request, show_id=1)

    def test_user_with_event(self):
        user = User.objects.get(pk=2)
        user.profile = Profile.objects.get(pk=2)
        user.profile.save()
        self.request.user = user
        response = mock_fn(self.request, show_id=1)
        self.assertEqual(response, self.request)


@view_show
def mock_fn(request, *args, **kwargs):
    return request

class editShowDecoratorTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'calendars', 'info',
                'shows', 'events']

    def setUp(self):
        # create WSGIRequest object
        factory = RequestFactory()
        self.request = factory.get(reverse('home'))

    def test_anonymous_user(self):
        self.request.user = auth.get_user(self.client)
        show = Show.objects.get(pk=1)
        # show visible
        show.approved = True
        show.visible = True
        show.save()
        response = mock_fn(self.request, show_id=1)
        self.assertEqual(response, self.request)
        # show not visible
        event = Event.objects.get(pk=1)
        event.approved = False
        event.visible = False
        event.save()
        event.show.save()
        self.assertRaises(PermissionDenied, mock_fn, self.request, show_id=1)

    def test_user_without_event(self):
        user = User.objects.get(pk=1)
        user.profile = Profile.objects.get(pk=1)
        user.profile.save()
        self.request.user = user
        show = Show.objects.get(pk=1)
        # show visible
        show.approved = True
        show.visible = True
        show.save()
        response = mock_fn(self.request, show_id=1)
        self.assertEqual(response, self.request)
        # show not visible
        event = Event.objects.get(pk=1)
        event.approved = False
        event.visible = False
        event.save()
        event.show.save()
        self.assertRaises(PermissionDenied, mock_fn, self.request, show_id=1)

    def test_user_with_event(self):
        user = User.objects.get(pk=2)
        user.profile = Profile.objects.get(pk=2)
        user.profile.save()
        self.request.user = user
        show = Show.objects.get(pk=1)
        # show visible
        show.approved = True
        show.visible = True
        show.save()
        response = mock_fn(self.request, show_id=1)
        self.assertEqual(response, self.request)
        # show not visible
        event = Event.objects.get(pk=1)
        event.approved = False
        event.visible = False
        event.save()
        event.show.save()
        response = mock_fn(self.request, show_id=1)
        self.assertEqual(response, self.request)
