from django.contrib.staticfiles.storage import staticfiles_storage
from django import template

import urllib, urlparse

from feeds.models import Follow
from annoying.functions import get_object_or_None


def is_following(user, target):
    if get_object_or_None(Follow, user=user, target=target):
        return 'isFollowing'
    return None


def append_to_get(url, params):
    print url
    print params
    url_parts = list(urlparse.urlparse(url))
    #query = dict(urlparse.parse_qs(url_parts[4]))
    #query.update(params)

    url_parts[4] = urllib.urlencode(params)

    return urlparse.urlunparse(url_parts)

FeedGlobals = {
    'is_following': is_following,
    'append_to_get': append_to_get,
}
