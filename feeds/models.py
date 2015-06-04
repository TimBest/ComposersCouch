import pytz
from django.conf import settings
from django.db import models
from django.utils.timezone import make_naive
from django.utils.translation import ugettext as _

from accounts.models import Profile


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='target_posts')
    message = models.TextField()
    photo = models.ForeignKey('photos.Image',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    local_votes = models.PositiveIntegerField(default=1)
    site_votes = models.PositiveIntegerField(default=1)

    def create_activity(self):
        from stream_framework.activity import Activity
        from feeds.verbs import Post as PostVerb
        activity = Activity(self.user, PostVerb, self.id, self.target,
                            time=make_naive(self.created_at, pytz.utc),)
        return activity

class Follow(models.Model):
    '''
    A simple table mapping who a user is following.
    For example, if user is Kyle and Kyle is following Alex,
    the target would be Alex.
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_set')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower_set')

from feeds import verbs
