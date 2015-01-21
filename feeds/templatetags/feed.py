from django.template import Library

from feeds.models import Follow
from annoying.functions import get_object_or_None


register = Library()

@register.simple_tag
def is_following(user, target):
    if get_object_or_None(Follow, user=user, target=target):
        return 'isFollowing'
    return None
