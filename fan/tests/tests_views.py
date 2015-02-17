from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User


class FanViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles', 'fans']

    def test_home_view(self):
        """  """
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('fan:home', kwargs={'username': user.username}))
        #redirect to news
        self.assertEqual(response.status_code, 302)

    def test_news_view(self):
        """  """
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('fan:news', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)

    def test_photos_view(self):
        """  """
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('fan:photos', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)
