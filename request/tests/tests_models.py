from django.test import TestCase


class PrivateRequestModelTest(TestCase):
    fixtures = ['users', 'profiles', 'contactInfos','locations', 'contacts',
                'zipcodes', 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates']

    # TODO
    def test_has_accepted(self):
        pass

    def test_headliner(self):
        pass

    def test_venue(self):
        pass

    def test_openers(self):
        pass
