from annoying.functions import get_object_or_None
from contact.models import Zipcode
from easy_timezones.middleware import get_client_ip, db


def get_location(request, code=None, attr='code'):
    zipcode = None
    if code and code !='None':
        zipcode = get_object_or_None(Zipcode, code=code)
    elif hasattr(request, 'user') and request.user.is_authenticated():
        zipcode = request.user.profile.contact_info.location.zip_code
    else:
        ip = get_client_ip(request)
        if ip == '127.0.0.1':
            ip = "24.206.228.69"
        record = db.record_by_addr(ip)
        code = record.get('postal_code')
        zipcode = get_object_or_None(Zipcode, code=code)
    return getattr(zipcode, attr, None)
