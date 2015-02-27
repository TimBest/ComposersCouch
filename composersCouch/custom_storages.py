from django.conf import settings
from django.contrib.staticfiles.storage import CachedFilesMixin

from pipeline.storage import PipelineMixin
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(PipelineMixin, CachedFilesMixin, S3BotoStorage):
    pass

class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
