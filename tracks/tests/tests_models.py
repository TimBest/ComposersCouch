from django.test import TestCase



class PrivateRequestModelTest(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',  
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates',
                'privateRequests', 'requestParticipants']

    def test_json_playlist(self):
        pass
        #album = Album.objects.get(pk=1)
        #tracks = Track.objects.all()
