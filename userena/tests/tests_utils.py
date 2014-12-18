from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable, User

from accounts.models import Profile
from userena.utils import get_gravatar, signin_redirect, get_protocol
from userena import settings as userena_settings
from userena.models import UserenaBaseProfile

import hashlib

class UtilsTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users']

    def test_get_gravatar(self):
        template = '//www.gravatar.com/avatar/%(hash)s?s=%(size)s&d=%(type)s'

        # The hash for alice@example.com
        hash = hashlib.md5('alice@example.com').hexdigest()

        # Check the defaults.
        self.failUnlessEqual(get_gravatar('alice@example.com'),
                             template % {'hash': hash,
                                         'size': 80,
                                         'type': 'identicon'})

        # Check different size
        self.failUnlessEqual(get_gravatar('alice@example.com', size=200),
                             template % {'hash': hash,
                                         'size': 200,
                                         'type': 'identicon'})

        # Check different default
        http_404 = get_gravatar('alice@example.com', default='404')
        self.failUnlessEqual(http_404,
                             template % {'hash': hash,
                                         'size': 80,
                                         'type': '404'})

        # Is it really a 404?
        response = self.client.get(http_404)
        self.failUnlessEqual(response.status_code, 404)

    def test_signin_redirect(self):
        """
        Test redirect function which should redirect the user after a
        succesfull signin.

        """
        # Test with a requested redirect
        self.failUnlessEqual(signin_redirect(redirect='/accounts/'), '/accounts/')

        # Test with only the user specified
        user = User.objects.get(pk=1)
        self.failUnlessEqual(signin_redirect(user=user),
                             '/accounts/%s/' % user.username)

        # The ultimate fallback, probably never used
        self.failUnlessEqual(signin_redirect(), settings.LOGIN_REDIRECT_URL)

    def test_get_protocol(self):
        """ Test if the correct protocol is returned """
        self.failUnlessEqual(get_protocol(), 'http')

        userena_settings.USERENA_USE_HTTPS = True
        self.failUnlessEqual(get_protocol(), 'https')
        userena_settings.USERENA_USE_HTTPS = False
