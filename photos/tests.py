#!/usr/bin/env python
# vim:fileencoding=utf-8

import os

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from django.test.client import Client

from models import *


class photosTest(TestCase):

    fixtures = [
        'users', 'contactInfos', 'contacts', 'locations', 'zipcodes',
        'profiles', 'applications', 'publicRequests', 'numApplicants',
        'privateRequests', 'requestParticipants', 'threads', 'messages',
        'participants', 'dates', 'genres', 'albums', 'artists', 'tracks',
        'media', 'calendars', 'info', 'shows', 'events', 'venues', 'fans',
    ]

    def setUp(self):
        self.image_file = open(os.path.join(os.path.dirname(__file__), 'test_img.jpg'))
        self.user = User.objects.get(pk=1)
        self.client = Client()

    def _upload_test_image(self, identification='john@example.com', password='blowfish'):
        self.client.post(reverse('login'),
                         data={'identification': identification,
                               'password': password})
        self.image_file = open(os.path.join(os.path.dirname(__file__), 'test_img.jpg'))
        response = self.client.get(reverse('photos:upload'))
        self.assertEqual(response.status_code, 200)
        values = {'image' : self.image_file}
        response = self.client.post(reverse('photos:upload'), values, follow=True)
        return response

    def test_image_upload(self):
        response = self._upload_test_image()
        self.assertEqual(response.status_code, 200)
        img_url = Image.objects.get(user__pk=1).get_absolute_url()
        response = self.client.get(img_url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self._upload_test_image()
        self.client.logout()
        self.client.post(reverse('login'),
                         data={'identification': 'jane@example.com',
                               'password': 'blowfish'})
        image_id = Image.objects.get(user__pk=1).id
        response = self.client.post(reverse('photos:delete-image', kwargs={'pk': image_id}), follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()
        self.client.post(reverse('login'),
                         data={'identification': 'john@example.com',
                               'password': 'blowfish'})
        response = self.client.post(reverse('photos:delete-image', kwargs={'pk': image_id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Image.objects.all()), 0)

    def test_update_image(self):
        self._upload_test_image()
        self.client.post(reverse('login'),
                         data={'identification': 'john@example.com',
                               'password': 'blowfish'})
        image_id = Image.objects.get(user__pk=1).id
        response = self.client.get(reverse('photos:update-image', kwargs={'pk': image_id}), follow=True)
        self.assertEqual(response.status_code, 200)
        values = {'title' : 'changed title' }
        self.client.post(reverse('photos:update-image', kwargs={'pk': image_id}), values, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Image.objects.get(user__pk=1).title == 'changed title')

    def test_prev_next_with_ordering(self):
        for i in range(1, 6):
            self._upload_test_image()
            img = Image.objects.order_by('-id')[0]
            img.order = i
            img.save()
        # Swap two id's
        im1 = Image.objects.get(order=2)
        im2 = Image.objects.get(order=4)
        im1.order, im2.order = 4, 2
        im1.save()
        im2.save()
        response = self.client.get(Image.objects.get(order=3).get_absolute_url())
        self.assertEqual(response.context['next'], im1)
        self.assertEqual(response.context['previous'], im2)
