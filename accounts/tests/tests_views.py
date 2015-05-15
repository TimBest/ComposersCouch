from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile


class ViewsTests(TestCase):
    """ Test the account views """
    fixtures = ['site', 'users', 'contactInfos', 'contacts', 'locations', 'zipcodes',
                'profiles', 'artists', 'venues', 'fans',]
    claim_profile = Profile(user=User(pk=1), has_owner=False)

    def test_signup_view(self):
        """ """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        valid_values = [
            {'email': 'signUpEmailArtist@example.com',
             'password1': 'foobar',
             'profile_type': 'm',
             'zip_code': 12065,
             'first_name': '',
             'last_name': '',
             'band_name': 'Band Name',
             'venue_name': ''},
        ]
        #TODO:: find out how to pass profile type to the view
        for values in valid_values:
            response = self.client.post(reverse('signup'), values, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                Profile.objects.get(user__email=values['email']).profile_type,
                values['profile_type']
            )

    def test_signup_social_view(self):
        """ """
        # TODO: test POST
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
        """        """
        # TODO: generate token and test this
        pass

    def test_login_view(self):
        """        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        valid_values = [
            {'identification': 'john@example.com',
             'password': 'blowfish',},
        ]
        for values in valid_values:
            response = self.client.post(reverse('login'), values, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                User.objects.get(email=values['identification']),
                response.context["user"]
            )

    def test_loginredirect_view(self):
        """ A ``GET`` to the signout view """
        response = self.client.get(reverse('loginredirect'))
        self.assertEqual(response.status_code, 302)
