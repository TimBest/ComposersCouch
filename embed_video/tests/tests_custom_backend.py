from unittest import TestCase

from embed_video.backends import detect_backend

from .custom_backend import CustomBackend


class CustomBackendTestCase(TestCase):
    def setUp(self):
        self.backend = detect_backend('http://myvideo.com/1530')

    def test_detect_backend(self):
        self.assertIsInstance(self.backend, CustomBackend)

    def test_code(self):
        self.assertEqual(self.backend.code, '1530')

    def test_url(self):
        self.assertEqual(self.backend.get_url(),
                         'http://play.myvideo.com/c/1530/')

    def test_url_https(self):
        self.backend.is_secure = True
        self.assertEqual(self.backend.get_url(),
                         'https://play.myvideo.com/c/1530/')

    def test_thumbnail(self):
        self.assertEqual(self.backend.get_thumbnail_url(),
                         'http://thumb.myvideo.com/c/1530/')

