from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.measure import D
from annoying.functions import get_object_or_None

from stream_framework.activity import Activity
from stream_framework.feed_managers.base import Manager, FanoutPriority, add_operation, remove_operation

from models import Follow, Post
from post_feed import PostFeed, UserPostFeed, LocalFeed
from verbs import Post as PostVerb
from contact.models import Zipcode


class PostFeedly(Manager):
    feed_classes = dict(normal=PostFeed)
    geo_feed_classes = dict(local=LocalFeed)
    user_feed_class = UserPostFeed

    def add_post(self, post):
        activity = post.create_activity()
        zipcode = post.target.profile.contact_info.location.zip_code
        # Add activity to geo based feeds
        self.add_geo_activity(zipcode, activity)
        # Add activity the user's feed, and start the fanout
        self.add_user_activity(post.target_id, activity)

    def create_and_add_post(self, user, target, message):
        post = Post(user=user, target=target, message=message)
        post.save()
        zip_code = user.profile.contact_info.location.zip_code
        self.add_post(post=post)
        return post

    def remove_post(self, post):
        activity = post.create_activity()
        zipcode = post.target.profile.contact_info.location.zip_code
        self.remove_geo_activity(zipcode, activity)
        self.remove_user_activity(post.user_id, activity)
        post.delete()

    def get_user_follower_ids(self, user_id):
        ids = Follow.objects.filter(target=user_id).values_list('user_id', flat=True)
        return {FanoutPriority.HIGH:ids}

    def get_zipcodes(self, zip_code, distance):
        zip_location = zip_code.point
        zip_codes = Zipcode.objects.filter(point__distance_lte=(zip_location, D(m=distance))).values_list('code', flat=True)
        return {FanoutPriority.HIGH:zip_codes}

    def get_local_feed(self, zip_code):
        return LocalFeed(zip_code)

    def add_geo_activity(self, zip_code, activity):
        '''
        Store the new activity and then fanout to the local feeds

        This function will
        - store the activity in the activity storage
        - fanout for all local_feed_classes

        :param zip_code: the zip_code Object associated with the user
        :param activity: the activity which to add
        '''
        operation_kwargs = dict(activities=[activity], trim=True)

        for feed_class in self.geo_feed_classes.values():
            for priority_group, zip_codes in self.get_zipcodes(zip_code=zip_code, distance=feed_class.distance).items():
                # create the fanout tasks
                self.create_fanout_tasks(
                    zip_codes,
                    feed_class,
                    add_operation,
                    operation_kwargs=operation_kwargs,
                    fanout_priority=priority_group
                )
        self.metrics.on_activity_published()

    def remove_geo_activity(self, zip_code, activity):
        '''create_fanout_tasks
        Remove the activity from the geo feeds

        :param zip_code: the zip_code Object associated with the user
        :param activity: the activity which to remove
        '''
        # we don't remove from the global feed due to race conditions
        # but we do remove from the local feeds
        local_feed = self.get_local_feed(zip_code)
        local_feed.remove(activity)

        # no need to trim when removing items
        operation_kwargs = dict(activities=[activity], trim=False)

        for feed_class in self.geo_feed_classes.values():
            for priority_group, zip_codes in self.get_zipcodes(zip_code=zip_code, distance=feed_class.distance).items():
                print priority_group
                print zip_codes
                self.create_fanout_tasks(
                    zip_codes,
                    feed_class,
                    remove_operation,
                    operation_kwargs=operation_kwargs,
                    fanout_priority=priority_group
                )
        self.metrics.on_activity_removed()

feedly = PostFeedly()
