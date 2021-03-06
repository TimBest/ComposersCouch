from stream_framework.feeds.redis import RedisFeed

""" User Feeds """
# The feed containing posts by those you follow
class PostFeed(RedisFeed):
    key_format = 'feed:normal:%(user_id)s'

# The feed containing only your posts
class UserPostFeed(PostFeed):
    key_format = 'feed:user:%(user_id)s'

""" Zip Code Feeds """
# The feed containing posts in a zipcode
class LocalFeed(RedisFeed):
    key_format = 'feed:normal:%(zip_code)s'
    # distance in meters (50 miles)
    distance = 75000

    def __init__(self, zip_code):
        '''
        :param zip_code: the zip_code associated to the feed we're working on
        '''
        self.zip_code = zip_code
        self.key_format = self.key_format
        self.key = self.key_format % {'zip_code': self.zip_code}

        self.timeline_storage = self.get_timeline_storage()
        self.activity_storage = self.get_activity_storage()

        # ability to filter and change ordering (not supported for all
        # backends)
        self._filter_kwargs = dict()
        self._ordering_args = tuple()
