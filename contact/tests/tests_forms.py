from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from contact import forms
from contact.models import Zipcode


class ContactInfoFormsTests(TestCase):
    fixtures = ['zipcodes']

    def test_zipcode_form(self):
        valid_data_dicts = [
            {'data': {'zip_code': Zipcode(pk=12065)},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.ZipcodeForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_location_form(self):
        invalid_data_dicts = [
            # no band name for type artist
            {'data': {'address_1': '3 Zamora Court',
                      'address_2': 'apt. 215',
                      'city': 'Clifton Park',
                      'state': 'NY',
                      'zip_code': ''},
            'error': ('zip_code', [_(u'This field is required.')])},
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.LocationForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        valid_data_dicts = [
            {'data': {'address_1': '3 Zamora Court',
                      'address_2': 'apt. 215',
                      'city': 'Clifton Park',
                      'state': 'NY',
                      'zip_code': Zipcode(pk=12065)},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.LocationForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_non_user_location_form(self):
        valid_data_dicts = [
            {'data': {'address_1': '3 Zamora Court',
                      'address_2': 'apt. 215',
                      'city': 'Clifton Park',
                      'state': 'NY',
                      'zip_code': ''},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.NonUserLocationForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_contact_form(self):
        valid_data_dicts = [
            {'data': {'name': 'Santi White',
                      'email': 'santigold@example.com',
                      'phone': '8765309',
                      'url': 'www.example.com',},},
        ]

        for valid_dict in valid_data_dicts:
            form = forms.ContactForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())


class LinksFormTests(TestCase):

    def taset_clean_url(self):
        valid_urls = [['https://www.example.com','https://www.example.com']
                      ['http://www.example.com','http://www.example.com']
                      ['www.example.com','http://www.example.com']
                      ['example.com','http://www.example.com']
        ]
        for url in valid_urls:
            cleaned_url = clean_url(url[0])
            self.assertEqual(cleaned_url, url[1])

    def test_socail_form(self):
        invalid_data_dicts = [
            {'data': {'facebook': 'composerscouch.com',
                      'google_plus': '',
                      'twitter': ''},
            'error': ('facebook', [_(u'Must be a Facebook URL.')])},
            {'data': {'facebook': '',
                      'google_plus': 'composerscouch.com',
                      'twitter': ''},
            'error': ('google_plus', [_(u'Must be a Google Plus URL.')])},
            {'data': {'facebook': '',
                      'google_plus': '',
                      'twitter': 'composerscouch.com'},
            'error': ('twitter', [_(u'Must be a Twitter URL.')])},
        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.SocialLinksForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        valid_data_dicts = [
            {'data': {'facebook': 'https://www.facebook.com/thekooksofficial',
                      'google_plus': 'https://plus.google.com/116651435444058665368/about',
                      'twitter': 'https://twitter.com/thekooksmusic'},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.SocialLinksForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_photo_form(self):
        invalid_data_dicts = [
            {'data': {'instagram': 'composerscouch.com',
                      'tumblr': ''},
            'error': ('instagram', [_(u'Must be a Instagram URL.')])},
            {'data': {'instagram': '',
                      'tumblr': 'composerscouch.com'},
            'error': ('tumblr', [_(u'Must be a Tumblr URL.')])},

        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.PhotoLinksForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        valid_data_dicts = [
            {'data': {'instagram': 'http://instagram.com/thekooksmusic/',
                      'tumblr': 'http://thekooksmusic.tumblr.com/'},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.PhotoLinksForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_video_form(self):
        invalid_data_dicts = [
            {'data': {'youtube': 'composerscouch.com',
                      'vimeo': ''},
            'error': ('youtube', [_(u'Must be a Youtube URL.')])},
            {'data': {'youtube': '',
                      'vimeo': 'composerscouch.com'},
            'error': ('vimeo', [_(u'Must be a Vimeo URL.')])},

        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.VideoLinksForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        valid_data_dicts = [
            {'data': {'youtube': 'https://www.youtube.com/user/thekooksofficial',
                      'vimeo': 'http://vimeo.com/davissilis'},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.VideoLinksForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())

    def test_music_form(self):
        invalid_data_dicts = [
            {'data': {'bandcamp': 'composerscouch.com',
                      'itunes': '',
                      'spotify': '',
                      'soundcloud': ''},
            'error': ('bandcamp', [_(u'Must be a Bandcamp URL.')])},
            {'data': {'bandcamp': '',
                      'itunes': 'composerscouch.com',
                      'spotify': '',
                      'soundcloud': ''},
            'error': ('itunes', [_(u'Must be a iTunes URL.')])},
            {'data': {'bandcamp': '',
                      'itunes': '',
                      'spotify': 'composerscouch.com',
                      'soundcloud': ''},
            'error': ('spotify', [_(u'Must be a Spotify URL.')])},
            {'data': {'bandcamp': '',
                      'itunes': '',
                      'spotify': '',
                      'soundcloud': 'composerscouch.com'},
            'error': ('soundcloud', [_(u'Must be a SoundCloud URL.')])},
        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.MusicLinksForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        valid_data_dicts = [
            {'data': {'bandcamp': 'http://sekinzer.bandcamp.com/track/junk-of-the-heart-cover',
                      'itunes': 'https://itunes.apple.com/us/artist/the-kooks/id68448386',
                      'spotify': 'https://play.spotify.com/artist/1GLtl8uqKmnyCWxHmw9tL4',
                      'soundcloud': 'https://soundcloud.com/kooksmusic'},},
        ]
        for valid_dict in valid_data_dicts:
            form = forms.MusicLinksForm(data=valid_dict['data'])
            self.failUnless(form.is_valid())
