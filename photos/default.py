from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import LazyObject
from django.utils.importlib import import_module


def get_module_class(class_path):
    """
    imports and returns module class from ``path.to.module.Class``
    argument
    """
    mod_name, cls_name = class_path.rsplit('.', 1)

    try:
        mod = import_module(mod_name)
    except ImportError as e:
        raise ImproperlyConfigured(('Error importing module %s: "%s"' % (mod_name, e)))

    return getattr(mod, cls_name)

class Backend(LazyObject):
    def _setup(self):
        self._wrapped = get_module_class('sorl.thumbnail.base.ThumbnailBackend')()


class KVStore(LazyObject):
    def _setup(self):
        self._wrapped = get_module_class('sorl.thumbnail.kvstores.cached_db_kvstore.KVStore')()


class Engine(LazyObject):
    def _setup(self):
        self._wrapped = get_module_class('sorl.thumbnail.engines.pil_engine.Engine')()


class Storage(LazyObject):
    def _setup(self):
        self._wrapped = get_module_class(settings.DEFAULT_FILE_STORAGE)()


backend = Backend()
kvstore = KVStore()
engine = Engine()
storage = Storage()
