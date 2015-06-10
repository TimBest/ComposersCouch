import pytz
import pygeoip
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils import timezone

from easy_timezones.utils import get_ip_address_from_request


GEOIP_DATABASE = getattr(settings, 'GEOIP_DATABASE', None)

if not GEOIP_DATABASE:
    raise ImproperlyConfigured("GEOIP_DATABASE setting has not been defined.")

db_loaded = False
db = None

def load_db():
    global db
    db = pygeoip.GeoIP(settings.GEOIP_DATABASE, pygeoip.MEMORY_CACHE)

    global db_loaded
    db_loaded = True

    return db

class EasyTimezoneMiddleware(object):
    def process_request(self, request):
        if not db_loaded:
            load_db()

        tz = request.session.get('django_timezone')

        if not tz:
            # use the default timezone (settings.TIME_ZONE) for localhost
            tz = timezone.get_default_timezone()

            ip = get_ip_address_from_request(request)
            if ip != '127.0.0.1':
                # if not local, fetch the timezone from pygeoip
                tz = db.time_zone_by_addr(ip)
            else:
                tz = pytz.timezone('US/Eastern')
        if tz:
            timezone.activate(tz)
        else:
            timezone.deactivate()
