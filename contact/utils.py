#from django.contrib.gis.utils import GeoIP

from annoying.functions import get_object_or_None
from contact.models import Zipcode

def get_location(request, code=None, attr='code'):
    zipcode = None
    if code and code !='None':
        zipcode = get_object_or_None(Zipcode, code=code)
    elif hasattr(request, 'zipcode'):
        zipcode = get_object_or_None(Zipcode, code=request.zipcode)
    elif request.user.is_authenticated():
        zipcode = request.user.profile.contact_info.location.zip_code
    return getattr(zipcode, attr, None)
