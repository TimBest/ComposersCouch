from __future__ import absolute_import  # Python 2 only

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template.defaultfilters import linebreaksbr
from jinja2 import Environment



def field_attrs(field_inst, **kwargs):
    """Adds html attributes to django form fields"""
    for k, v in kwargs.items():
        if v is not None:
            field_inst.field.widget.attrs[k] = v
        else:
            try:
                del field_inst.field.widget.attrs[k]
            except KeyError:
                pass
    return field_inst

def environment(**options):
    environment = Environment (
        extensions = [
            'pipeline.jinja2.ext.PipelineExtension',
            'feeds.templatetags.ext.FeedExtension',
            'jinja2.ext.i18n',
            'jinja2.ext.with_',
        ],
        **options
    )
    environment.filters['field_attrs'] = field_attrs
    environment.filters['linebreaksbr'] = linebreaksbr
    environment.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'is_development': settings.DEVELOPMENT,
        'now':timezone.now(),
    })
    return environment
