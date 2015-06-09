from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

from photos.fields import ImageField
try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

from photos.utils import get_file_path, get_model_string


def validate_file_extension(value):
    if value.name.endswith('.eps'):
        raise ValidationError(u'.eps files are not supported at this time')
    if value.name.endswith('.gif'):
        raise ValidationError(u'.gif files are not supported at this time')

class BaseImage(models.Model):
    class Meta(object):
        abstract = True
        ordering = ('order', 'id')
        permissions = (
            ('moderate_images', 'View, update and delete any image'),
        )

    title = models.CharField(_('Title'), max_length=100, blank=True, null=True)
    order = models.IntegerField(_('Order'), default=0)
    image = ImageField(verbose_name = _('File'), upload_to=get_file_path, validators=[validate_file_extension])
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True, related_name='images')
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)

    @permalink
    def get_absolute_url(self):
        return 'photos:image', (), {'pk': self.id}

    def __unicode__(self):
        return '%s'% self.id
