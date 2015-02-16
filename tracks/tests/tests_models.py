from django.contrib.auth.models import User
from django.test import TestCase

from tracks.models import Album, Track


class PrivateRequestModelTest(TestCase):
    fixtures = ['users', 'profiles', 'contactInfos','locations', 'contacts',
                'zipcodes', 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates',
                'privateRequests', 'requestParticipants']

    def test_json_playlist(self):
        pass
        #album = Album.objects.get(pk=1)
        #tracks = Track.objects.all()
