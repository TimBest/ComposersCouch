"""
WSGI config for composersCouch project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "composersCouch.settings")

import django
from django.core.handlers.wsgi import WSGIHandler

def get_wsgi_application():
    django.setup()
    return WSGIHandler()

application = get_wsgi_application()


"""
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
