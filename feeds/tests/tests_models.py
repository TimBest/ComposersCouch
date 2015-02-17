from django.test import TestCase


class PostModelTest(TestCase):
    """ Test the ``Post`` model """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles']

class FollowModelTest(TestCase):
    """ Test the ``follow`` model """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles']
