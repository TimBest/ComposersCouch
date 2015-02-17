from django.http import HttpRequest
from django.test import TestCase
from django.utils.importlib import import_module
from django.conf import settings
from django.contrib.auth.models import User

from accounts.models import Profile
from userena.middleware import UserenaLocaleMiddleware
from userena import settings as userena_settings

User = User


class UserenaLocaleMiddlewareTests(TestCase):
    """ Test the ``UserenaLocaleMiddleware`` """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles']

    def _get_request_with_user(self, user):
        """ Fake a request with an user """
        request = HttpRequest()
        request.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
        }
        request.method = 'GET'
        request.session = {}

        # Add user
        request.user = user
        return request

    def test_without_profile(self):
        """TODO: Middleware should do nothing when a user has no profile """
        pass

    def test_without_language_field(self):
        """ Middleware should do nothing if the profile has no language field """
        userena_settings.USERENA_LANGUAGE_FIELD = 'non_existant_language_field'
        user = User.objects.get(pk=1)

        req = self._get_request_with_user(user)

        # Middleware should do nothing
        UserenaLocaleMiddleware().process_request(req)
        self.failIf(hasattr(req, 'LANGUAGE_CODE'))
