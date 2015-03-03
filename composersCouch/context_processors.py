from django.conf import settings
from django.utils import timezone


def now(request):
    return {'now' : timezone.now()}

def development(request):
    return {'is_development' : settings.DEVELOPMENT}
