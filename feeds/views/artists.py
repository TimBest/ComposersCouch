from datetime import datetime, time
from django.contrib.gis.measure import D
from django.utils.timezone import utc
from django.views.generic import TemplateView

from accounts.models import MusicianProfile
from contact.utils import get_location
from feeds.post_feed import LocalFeed, RegionalFeed
from feeds.views import AvailabilityMixin, FeedMixin


def artists(request, scope='all', *args, **kwargs):
    if scope == 'local':
        return LocalView.as_view()(request, *args, **kwargs)
    elif scope == 'regional':
        return ReqionalView.as_view()(request, *args, **kwargs)
    elif scope == 'following':
        return FollowingView.as_view()(request, *args, **kwargs)
    else:
        return AllView.as_view()(request, *args, **kwargs)

class ArtistView(FeedMixin, TemplateView):
    modelManager = MusicianProfile.objects

    def get_default_order(self):
        return "all"

    def get_order(self, qs):
        order = self.kwargs.get('order')
        if order == "new":
            return qs.order_by('-profile__user__date_joined')
        else:
            # all
            return qs

class AvailabilityView(AvailabilityMixin, ArtistView):
    template_name = 'feeds/artists/available.html'

    def get_posts(self, **kwargs):
        start = datetime.combine(self.start_date, time()).replace(tzinfo=utc)
        end = datetime.combine(self.end_date, time()).replace(tzinfo=utc)
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        return self.modelManager.exclude(**self.get_exclude(start, end)).filter(
            profile__user__calendar__events__line__line__distance_lte=(location, D(m=LocalFeed.distance))
        )

available_artists = AvailabilityView.as_view()

class LocalView(ArtistView):
    template_name = 'feeds/artists/local.html'

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        return self.modelManager.filter(
            profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
        )

class ReqionalView(ArtistView):
    template_name = 'feeds/artists/regional.html'

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        return self.modelManager.filter(
            profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=RegionalFeed.distance))
        )

class FollowingView(ArtistView):
    template_name = 'feeds/artists/following.html'

    def get_posts(self, **kwargs):
        return self.modelManager.filter(
            profile__user__pk__in=self.request.user.following_set.values_list('target')
        )

class AllView(ArtistView):
    template_name = 'feeds/artists/all.html'

    def get_posts(self, **kwargs):
        return self.modelManager.all()