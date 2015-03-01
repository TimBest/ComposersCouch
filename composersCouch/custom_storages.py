from django.conf import settings
from django.contrib.staticfiles.storage import CachedFilesMixin

from pipeline.storage import GZIPMixin PipelineMixin
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(GZIPMixin, PipelineMixin, S3BotoStorage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
