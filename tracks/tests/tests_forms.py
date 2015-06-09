import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from tracks import forms


class FormTests(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'videos']

    def setUp(self):
        self.mp3_file = open(os.path.join(os.path.dirname(__file__), 'files/thriftyTale.mp3'))
        self.ogg_file = open(os.path.join(os.path.dirname(__file__), 'files/sway.ogg'))

    def test_tracks_form(self):
        # Test a valid form.
        # TODO: test uploading multiple files
        valid_dicts = [
            [{},
             {"tracks": SimpleUploadedFile(self.mp3_file.name, self.mp3_file.read()),},],
            [{},
             {"tracks": SimpleUploadedFile(self.ogg_file.name, self.ogg_file.read()),},],
        ]
        for valid_dict in valid_dicts:
            form = forms.TracksForm(valid_dict[0], valid_dict[1])
            self.failUnless(form.is_valid())

    def test_album_form(self):
        # Test a valid form.
        valid_dicts = [
            [{"title":"Overseas Then Under",
              "year":"2013",
              "genre": [2,],
              "description":"This is our album",},
             {"tracks": SimpleUploadedFile(self.mp3_file.name, self.mp3_file.read()),},],
        ]
        for valid_dict in valid_dicts:
            form = forms.AlbumForm(valid_dict[0], valid_dict[1])
            self.failUnless(form.is_valid())

    def test_album_audio_form(self):
        # Test a valid form.
        valid_data_dicts = [
            {"album": 1,
             "title":"Overseas Then Under",
              "order":1,},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.AlbumAudioForm(data=valid_dict)
            print form.errors
            self.failUnless(form.is_valid())

    def test_album_video_form(self):
        invalid_data_dicts = [
            #test an invalid url
            {'data': {"album": 1,
                      "title":"Overseas Then Under",
                      "video": "http://www.composerscouch.com/",
                      "order": 1,},
             'error': ('video', [_(u'URL could not be recognized.')])},
        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.AlbumVideoForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]], invalid_dict['error'][1])
        # Test a valid form.
        valid_data_dicts = [
            {"album": 1,
             "title":"Overseas Then Under",
             "video": "https://vimeo.com/38489428",
             "order": 1,},
            {"album": 1,
             "title":"Overseas Then Under",
             "video": "https://www.youtube.com/watch?v=pquhYpGHrlw",
             "order":2,},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.AlbumVideoForm(data=valid_dict)
            self.failUnless(form.is_valid())

    def test_video_form(self):
        invalid_data_dicts = [
            #test an invalid url
            {'data': {"user": 1,
                      "video": "http://www.composerscouch.com/",},
             'error': ('video', [_(u'URL could not be recognized.')])},
        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.VideoForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]], invalid_dict['error'][1])
        # Test a valid form.
        valid_data_dicts = [
            {"user": 1,
             "video": "https://vimeo.com/38489428",},
            {"user": 1,
             "video": "https://www.youtube.com/watch?v=pquhYpGHrlw",},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.VideoForm(data=valid_dict)
            self.failUnless(form.is_valid())
