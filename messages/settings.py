from django.conf import settings

MESSAGES_USE_SENDGRID = getattr(settings, 'MESSAGES_USE_SENDGRID', False)
MESSAGES_ID = getattr(settings, 'MESSAGES_ID', 'm')

INBOX_COUNT_CACHE = "MESSAGES_INBOX_COUNT_%s"
INBOX_COUNT_CACHE_TIME = 60 * 60 * 6
