from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from utils import get_model_string
from photos.models import Image

def photos_processor(request):
    template = getattr(settings, 'PHOTOS_TEMPLATE', False)
    ret = {
        'PHOTOS_SHOW_USER': getattr(settings, 'PHOTOS_SHOW_USER', True),
        'PHOTOS_SHOW_TAGS': getattr(settings, 'PHOTOS_SHOW_TAGS', True),
        'PHOTOS_MODEL_STRING': get_model_string('Image'),
        'PHOTOS_LOAD_CSS': getattr(settings, 'PHOTOS_LOAD_CSS', True),
        }
    try:
        ret['photos_index_url'] = reverse('photos:index')
    except NoReverseMatch: #Bastard django-cms from hell!!!!111
        pass
    if template:
        ret['PHOTOS_TEMPLATE'] = template
    ret['photos_perms'] = {
        'add_image': request.user.has_perm('%s.add_%s' % (Image._meta.app_label, Image.__name__)),
    }
    return ret

  
