from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import Profile


class ViewsTests(TestCase):
    """ Test the account views """

    def test_profile_edit_view(self):
        pass
