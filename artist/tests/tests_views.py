from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User



class AboutViewsTests(TestCase):
    """  """

    def test_about_view(self):
        """  """
        pass
        #response = self.client.get(reverse('artist:about', kwargs={'username': self.user.username}))
        #self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        """  """
        #response = self.client.get(reverse('artist:about', kwargs={'username': self.user.username}))
        #self.assertEqual(response.status_code, 200)

class MusicViewsTests(TestCase):
    """  """

    def test_signup_auth_view(self):
        """  """
        pass
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

class VideosViewsTests(TestCase):
    """  """

    def test_signup_auth_view(self):
        """ """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
