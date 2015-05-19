from __future__ import absolute_import  # Python 2 only

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils import timezone

from jinja2 import Environment



def environment(**options):
    env = Environment (
        extensions = [
            'pipeline.jinja2.ext.PipelineExtension',
            'jinja2.ext.i18n',
        ],
        **options
    )
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'is_development': settings.DEVELOPMENT,
        'now':timezone.now(),
    })
    return env
