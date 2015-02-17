from django.contrib.auth.models import User
from django.test import TestCase

from tracks.models import Album, Track
from tracks.utils import json_playlist


class PrivateRequestModelTest(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',  
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media']

    def test_json_playlist(self):
        # TODO: add assertion
        album = Album.objects.get(pk=1)
        tracks = Track.objects.all()
        tracks_playlist = json_playlist(tracks)
        #self.assertEqual(len(list(tracks_playlist)), len(tracks))
        album_playlist = json_playlist(tracks, album=album)
        #self.assertEqual(len(list(album_playlist)), len(album.tracks.all()))
