from django.contrib.auth.models import User

from contact.models import Zipcode
from feeds.models import Post
from feeds.post_feedly import feedly
from stream_framework.feed_managers.base import remove_operation


def enrich_activities(activities):
    '''
    Load the models attached to these activities
    (Normally this would hit a caching layer like memcached or redis)
    '''
    post_ids = [a.object_id for a in activities]
    post_dict = Post.objects.in_bulk(post_ids)
    for a in activities:
        a.post = post_dict.get(a.object_id)
    return activities

def remove_all_activities():
    for user in User.objects.all():
        # remove posts from users feed
        feed = feedly.get_user_feed(user.id)
        activities = list(feed[:50])
        remove_operation(feed, activities)
        # removed posts from following feeds
        feed = feedly.get_feeds(user.id)['normal']
        activities = list(feed[:50])
        remove_operation(feed, activities)
    # remove posts from local feeds
    for zipcode in Zipcode.objects.all():
        feed = feedly.get_local_feed(zipcode.pk)
        activities = list(feed[:50])
        remove_operation(feed, activities)
