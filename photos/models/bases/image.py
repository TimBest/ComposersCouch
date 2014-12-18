from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

from sorl.thumbnail import ImageField, get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError
from tagging.fields import TagField

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

try:
    import Image as PILImage
except ImportError:
    from PIL import Image as PILImage

from photos.utils import get_file_path, get_model_string

SELF_MANAGE = getattr(settings, 'PHOTOS_SELF_MANAGE', True)

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
    description = models.TextField(_('Description'), blank=True, null=True)
    tags = TagField(_('Tags'), blank=True)
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

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '100x100', crop='center').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            return 'ThumbnailError, %s' % ex.message

    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True


#noinspection PyUnusedLocal
def setup_photos_permissions(instance, created, **kwargs):
        if not created:
            return
        try:
            from photos.models import Image
            image_type = ContentType.objects.get(
                app_label = Image._meta.app_label,
                name='Image'
            )
            add_image_permission = Permission.objects.get(codename='add_image', content_type=image_type)
            change_image_permission = Permission.objects.get(codename='change_image', content_type=image_type)
            delete_image_permission = Permission.objects.get(codename='delete_image', content_type=image_type)
            instance.user_permissions.add(add_image_permission,)
            instance.user_permissions.add(change_image_permission,)
            instance.user_permissions.add(delete_image_permission,)
        except ObjectDoesNotExist:
            # Permissions are not yet installed or conten does not created yet
            # probaly this is first
            pass


if SELF_MANAGE:
    post_save.connect(setup_photos_permissions, User)
