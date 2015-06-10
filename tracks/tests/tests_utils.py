from django.test import TestCase

import ast

from tracks.models import Album, Track
from tracks.utils import json_playlist


class PrivateRequestModelTest(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks']

    def test_json_playlist(self):
        album = Album.objects.get(pk=1)
        tracks = Track.objects.all()
        tracks_playlist = json_playlist(tracks)
        self.assertEqual(len(ast.literal_eval(tracks_playlist)), len(tracks))
        album_playlist = json_playlist(tracks, album=album)
        self.assertEqual(len(ast.literal_eval(album_playlist)), len(album.track_set.all()))
