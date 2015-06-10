from bases.image import BaseImage
from django.utils.translation import ugettext_lazy as _

class Image(BaseImage):
    class Meta(BaseImage.Meta):
        abstract = False
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        app_label = 'photos'
