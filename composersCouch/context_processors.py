import datetime
from django.conf import settings


def now(request):
    return {'now' : datetime.datetime.now()}

def development(request):
    return {'is_development' : settings.DEVELOPMENT}
