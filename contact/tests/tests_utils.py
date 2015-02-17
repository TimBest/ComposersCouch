from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from contact.utils import get_location
from contact.models import Contact, ContactInfo, Location, Zipcode


class UtilsTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',  'zipcodes']

    def test_get_location(self):
        factory = RequestFactory()
        request = factory.get(reverse('home'))

        # No user and no code given
        self.assertEqual(get_location(request), None)
        # No user and a code
        self.assertEqual(get_location(request, "12065"), '12065')
        # User but no code
        user = User.objects.get(email='john@example.com')
        location = Location(pk=1)
        location.zip_code = Zipcode(pk=12065)
        location.save()
        user.profile.contact_info = ContactInfo(location=location,
                                                contact=Contact(pk=1))
        user.profile.save()
        request.user = user
        self.assertEqual(get_location(request),
                         user.profile.contact_info.location.zip_code.code)
        # user and code
        from annoying.functions import get_object_or_None
        self.assertEqual(get_location(request, "01225"),'01225')
        # ask for code by sttribute
