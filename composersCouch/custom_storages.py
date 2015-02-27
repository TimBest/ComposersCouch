from django.conf import settings
from django.contrib.staticfiles.storage import CachedFilesMixin
from django.core.files.storage import get_storage_class

from pipeline.storage import PipelineMixin
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(PipelineMixin, CachedFilesMixin, S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
