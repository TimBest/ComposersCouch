from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import D
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.utils.timezone import utc

from accounts.views import SignupEmailView, LoginView
from artist.models import ArtistProfile
from contact.utils import get_location
from feeds.post_feed import LocalFeed
from feeds.views import AvailabilityMixin, FeedMixin


login_required_m = method_decorator(login_required)

def artists(request, scope='any-distance', *args, **kwargs):
    kwargs['scope'] = scope
    if request.user.is_authenticated():
        views = AUTH_VIEWS
    else:
        views = VIEWS
    return views.get(scope, views['any-distance'])(request, *args, **kwargs)

class ArtistView(FeedMixin):
    model = ArtistProfile
    feedType = 'artists'
    default_order = "all"

    def get_order(self, qs, **kwargs):
        order = self.kwargs.get('order')
        if order == "latest":
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
    model = ArtistProfile

    def get_posts(self, **kwargs):
        # TODO: make properally timezone aware
        start = datetime.combine(self.start_date, time()).replace(tzinfo=utc)
        end = datetime.combine(self.end_date, time()).replace(tzinfo=utc)
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if location:
            return self.model.objects.exclude(**self.get_exclude(start, end)).filter(
                Q(profile__user__calendar__events__line__line__distance_lte=(location, D(m=LocalFeed.distance))) |
                Q(profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance)))
            ).distinct()
        else:
            return []

available_artists = AvailabilityView.as_view()

class LocalViewAuth(ArtistView):
    template_name = 'feeds/artists/local.html'

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if location:
            return self.model.objects.filter(
                profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
        else:
            return []

class LocalView(SignupEmailView, LoginView, LocalViewAuth):
    pass

class FollowingViewAuth(ArtistView):
    template_name = 'feeds/artists/following.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(FollowingViewAuth, self).dispatch(*args, **kwargs)

    def get_posts(self, **kwargs):
        return self.model.objects.filter(
            profile__user__pk__in=self.request.user.following_set.values_list('target')
        )

class FollowingView(SignupEmailView, LoginView, FollowingViewAuth):
    pass

class AllViewAuth(ArtistView):
    template_name = 'feeds/artists/all.html'

class AllView (AllViewAuth, SignupEmailView, LoginView,):
    pass

AUTH_VIEWS = {
    '50' : LocalViewAuth.as_view(),
    'following' : FollowingViewAuth.as_view(),
    'any-distance' : AllViewAuth.as_view(),
}

VIEWS = {
    '50' : LocalView.as_view(),
    'following' : FollowingView.as_view(),
    'any-distance' : AllView.as_view(),
}
