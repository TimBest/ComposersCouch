from __future__ import absolute_import  # Python 2 only

from django.core.urlresolvers import reverse
from django.test import signals, TestCase
from django.contrib.auth.models import User

from jinja2 import Template as Jinja2Template
import os

from accounts.models import Profile
from artist.models import ArtistProfile, Member
from artist.views import MusicianContactsView
from tracks.models import Album

#note - this code can be run only once
ORIGINAL_JINJA2_RENDERER = Jinja2Template.render
def instrumented_render(template_object, *args, **kwargs):
    context = dict(*args, **kwargs)
    signals.template_rendered.send(
                            sender=template_object,
                            template=template_object,
                            context=context
                        )
    return ORIGINAL_JINJA2_RENDERER(template_object, *args, **kwargs)
Jinja2Template.render = instrumented_render

class ViewsTests(TestCase):
    """  """
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes',
                'profiles', 'artists', 'members', 'calendars', 'albums',
                'media', 'tracks','genres']

    def _test_only_viewable_by_artist(self, url_name, kwargs):
        # Anonymous user is redirected to login
        self.client.logout()
        response = self.client.get(reverse(url_name, kwargs=kwargs))
        self.assertRedirects(response, '%s?next=%s' % (reverse('login'),
                             response.request['PATH_INFO']), status_code=302,
                             target_status_code=200,)
        # Non Artist is given permission denied
        self.client.post(reverse('login'),
                         data={'identification': 'john@example.com',
                               'password': 'blowfish'})
        response = self.client.get(reverse(url_name, kwargs=kwargs))
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        # Artist is given the page
        self.client.post(reverse('login'),
                         data={'identification': 'jane@example.com',
                               'password': 'blowfish'})
        response = self.client.get(reverse(url_name, kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

    def _login_artist(self):
        self.client.logout()
        self.client.post(reverse('login'),
                         data={'identification': 'jane@example.com',
                               'password': 'blowfish'})

    def test_view(self):
        """  """
        user = User.objects.get(pk=2)
        user.profile.artist_profile = ArtistProfile(pk=2)
        url_names = [
            ['artist:about',  {'username':user.username}],
            ['artist:news',   {'username':user.username}],
            ['artist:shows',  {'username':user.username}],
            ['artist:shows',  {'username':user.username,'year':2015}],
            ['artist:photos', {'username':user.username}],
            ['artist:music',  {'username':user.username}],
            ['artist:videos', {'username':user.username}],
        ]

        for url_name in url_names:
            response = self.client.get(reverse(url_name[0], kwargs=url_name[1]))
            self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('artist:home', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 302)

    def test_biography_form_view(self):
        url_name = 'artist:biographyForm'
        self._test_only_viewable_by_artist(url_name, {})
        values = {
            'biography': 'This is a sample biography. This is a\
                          second sentance about myself. And this is a Third.\
                          Now i will go on to describe another thing about my\
                          self. Hopefully this is not to long.',
        }
        self._login_artist()
        response = self.client.post(reverse(url_name), values, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["request"].user.profile.artist_profile.biography,
            values['biography']
        )

    def test_contact_form_view(self):
        user = None
        values = {
            'name': 'Santi White',
            'email': 'santigold@example.com',
            'phone': '8765309',
            'url': 'www.example.com',
            'address_1': '3 Zamora Court',
            'address_2': 'apt. 215',
            'city': 'Clifton Park',
            'state': 'NY',
            'zip_code': 12065,
        }
        url_names = [['artist:userContactForm', {}],]
        for contact_type in MusicianContactsView.CONTACT_TYPES:
            url_names.append(['artist:contactForm',{'contact_type':contact_type}],)
        self._login_artist()
        for url_name in url_names:
            self._test_only_viewable_by_artist(url_name[0], url_name[1])
            response = self.client.post(
                reverse(url_name[0], kwargs=url_name[1]), values, follow=True
            )
            user = response.context["request"].user
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(
                reverse(url_name[0], kwargs=url_name[1]),
                response.request['PATH_INFO']
            )
        self.assertEqual(
            user.profile.contact_info.contact.name,
            values['name']
        )

        for contact_type in MusicianContactsView.CONTACT_TYPES:
            contact_info = getattr(
                user.profile.artist_profile,
                MusicianContactsView.CONTACT_TYPES[contact_type]
            )
            self.assertEqual(contact_info.contact.name, values['name'])

    def test_member_forms_view(self):
        url_name = 'artist:memberForm'
        kwargs = {'member_id':1}
        self._test_only_viewable_by_artist(url_name, {})
        self._test_only_viewable_by_artist(url_name, kwargs)
        values = {
            'name': 'Andy Dwyer',
            'biography': 'Dogs are the best.',
            'current_member': True,
            'remove_member': False,
        }
        self._login_artist()
        response = self.client.post(reverse(url_name), values, follow=True)
        self.assertEqual(response.status_code, 200)
        member = Member.objects.get(name=values['name'])
        self.assertEqual(member.biography, values['biography'])
        values['biography'] = "No cats are."
        response = self.client.post(
            reverse(url_name, kwargs={'member_id':member.id}),
            values, follow=True
        )
        member_edited = Member.objects.get(name=values['name'])
        self.assertEqual(member_edited.biography, values['biography'])
        self.assertEqual(member_edited.id, member.id)

    def test_music_form_views(self):
        url_names = [
            ['artist:albumForm',         {}],
            ['artist:editAlbumForm',     {'album_id':1}],
            ['artist:tracksForm',        {'album_id':1}],
        ]
        for url_name in url_names:
            self._test_only_viewable_by_artist(url_name[0], url_name[1])
        mp3_file = open(os.path.join(os.path.dirname(__file__), 'files/thriftyTale.mp3'))
        values = {
            'title': "Around The Well",
            'year': "2009",
            'genre': [2,],
            'description':"This is our album",
            'tracks': mp3_file,
        }
        self._login_artist()
        # create album
        response = self.client.post(reverse('artist:albumForm'), values, follow=True)
        self.assertEqual(response.status_code, 200)
        album = Album.objects.get(title=values['title'])
        self.assertEqual(album.year, values['year'])
        # edit album
        values['description'] = "This is our album."
        values['tracks'] = ""
        response = self.client.post(
            reverse('artist:editAlbumForm', kwargs={'album_id':album.id}),
            values, follow=True
        )
        self.assertEqual(response.status_code, 200)
        album_edit = Album.objects.get(title=values['title'])
        self.assertEqual(album_edit.id, album.id)
        self.assertEqual(album_edit.description, values['description'])
        #ogg_file = open(os.path.join(os.path.dirname(__file__), 'files/sway.ogg'))
        #files = {"tracks": SimpleUploadedFile(self.mp3_file.name, self.mp3_file.read())}

    def test_video_form_views(self):
        url_names = [
            ['artist:video_album_form',  {}],
            ['artist:video_edit_album',  {'album_id':1}],
            ['artist:video_tracks_form', {'album_id':1}],
        ]

        for url_name in url_names:
            self._test_only_viewable_by_artist(url_name[0], url_name[1])
