from django.conf import settings
from django.core.files.storage import get_storage_class

from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    location = settings.STATICFILES_LOCATION

    def __init__(self, *args, **kwargs):
        super(StaticStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(StaticStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name

class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
