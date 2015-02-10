from django.core.urlresolvers import reverse
from django.test import TestCase


class TemplateViewsTests(TestCase):
    """  """

    def test_about_view(self):
        # Home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # About
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        # Team
        response = self.client.get(reverse('team'))
        self.assertEqual(response.status_code, 200)
        # Credit
        response = self.client.get(reverse('credit'))
        self.assertEqual(response.status_code, 200)
