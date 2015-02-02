#from django.contrib.gis.utils import GeoIP

from annoying.functions import get_object_or_None
from contact.models import Zipcode

def get_location(request, code=None, attr=None):
    zipcode = None
    if code is None:
        try:
          zipcode = request.user.profile.contact_info.location.zip_code
        except:
          pass
    else:
        zipcode = get_object_or_None(Zipcode, code=code)
    if zipcode:
        return getattr(zipcode, attr, None)
    #else:
    #g = GeoIP()
    #print g
    #return None
