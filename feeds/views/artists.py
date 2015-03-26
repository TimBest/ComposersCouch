from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import D
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.utils.timezone import utc
from django.views.generic import TemplateView

from artist.models import ArtistProfile
from contact.utils import get_location
from feeds.post_feed import LocalFeed
from feeds.views import AvailabilityMixin, FeedMixin


login_required_m = method_decorator(login_required)

def artists(request, scope='all', *args, **kwargs):
    kwargs['scope'] = scope
    if scope == 'local':
        return LocalView.as_view()(request, *args, **kwargs)
    elif scope == 'following':
        return FollowingView.as_view()(request, *args, **kwargs)
    else:
        return AllView.as_view()(request, *args, **kwargs)

class ArtistView(FeedMixin, TemplateView):
    modelManager = ArtistProfile.objects
    feedType = 'artists'

    def get_default_order(self):
        return "all"

    def get_order(self, qs, **kwargs):
        order = self.kwargs.get('order')
        if order == "new":
            return qs.order_by('-profile__user__date_joined')
        #elif order == "distance":
        #    distance_m = 500000
        #    location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        #    return qs.filter(
        #             profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=distance_m))
        #           ).distance(location).order_by('distance')
        else:
            # all
            return qs

class AvailabilityView(AvailabilityMixin, ArtistView):
    template_name = 'feeds/artists/available.html'

    def get_posts(self, **kwargs):
        # TODO: make properally timezone aware
        start = datetime.combine(self.start_date, time()).replace(tzinfo=utc)
        end = datetime.combine(self.end_date, time()).replace(tzinfo=utc)
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if location:
            return self.modelManager.exclude(**self.get_exclude(start, end)).filter(
                Q(profile__user__calendar__events__line__line__distance_lte=(location, D(m=LocalFeed.distance))) |
                Q(profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance)))
            )
        else:
            return []

available_artists = AvailabilityView.as_view()

class LocalView(ArtistView):
    template_name = 'feeds/artists/local.html'

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if location:
            return self.modelManager.filter(
                profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
        else:
            return []

class FollowingView(ArtistView):
    template_name = 'feeds/artists/following.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(FollowingView, self).dispatch(*args, **kwargs)

    def get_posts(self, **kwargs):
        return self.modelManager.filter(
            profile__user__pk__in=self.request.user.following_set.values_list('target')
        )

class AllView(ArtistView):
    template_name = 'feeds/artists/all.html'

    def get_posts(self, **kwargs):
        return self.modelManager.all()
