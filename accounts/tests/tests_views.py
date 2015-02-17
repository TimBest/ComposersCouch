from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile


class ViewsTests(TestCase):
    """ Test the account views """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles']
    claim_profile = Profile(user=User(pk=1), has_owner=False)

    def test_signup_auth_view(self):
        """ A ``GET`` to the ``signup`` view """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_email_view(self):
        """ """
        response = self.client.get(reverse('signup_email'))
        self.assertEqual(response.status_code, 200)

    def test_signup_social_view(self):
        """ """
        response = self.client.get(reverse('signupSocial'))
        self.assertEqual(response.status_code, 200)

    def test_claim_profile_view(self):
        """ claim_profile """
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('claim_profile', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 302)

    def test_verify_profile_claim_view(self):
        """  """
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('claim_profile_verify', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)

    def test_claim_profile_confirm_view(self):
        """
        TODO: generate token and test this

        """
        pass

    def test_signin_view(self):
        """
        TODO: A valid ``POST`` to the signin view should redirect the user to it's
        own profile page if no ``next`` value is supplied. Else it should
        redirect to ``next``.

        """
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)

    def test_loginredirect_view(self):
        """ A ``GET`` to the signout view """
        response = self.client.get(reverse('loginredirect'))
        self.assertEqual(response.status_code, 302)
