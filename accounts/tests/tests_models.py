from django.test import TestCase


class ProfileModelTest(TestCase):
    """ Test the ``BaseProfile`` model """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles']
