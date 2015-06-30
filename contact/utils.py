from annoying.functions import get_object_or_None
from contact.models import Zipcode
from easy_timezones.utils import get_ip_address_from_request
from easy_timezones import middleware


def get_location(request, code=None, attr='code'):
    zipcode = None
    if code and code !='None':
        zipcode = get_object_or_None(Zipcode, code=code)
    elif hasattr(request, 'user') and request.user.is_authenticated():
        zipcode = request.user.profile.contact_info.location.zip_code
    else:
        ip = get_ip_address_from_request(request)
        if ip == '127.0.0.1':
            ip = "96.249.1.67"
        if not middleware.db_loaded:
            middleware.db = middleware.load_db()
        try:
            record = middleware.db.record_by_addr(ip)
            code = record.get('postal_code')
            zipcode = get_object_or_None(Zipcode, code=code)
        except:
            zipcode = None
    return getattr(zipcode, attr, None)
