from photos.utils import load_class
from django.conf import settings

Image = load_class(getattr(settings, 'PHOTOS_IMAGE_MODEL', 'photos.models.image.Image'))

# This labels and classnames used to generate permissons labels
image_applabel = Image._meta.app_label
image_classname = Image.__name__.lower()
