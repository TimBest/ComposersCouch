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

class ArtistViewAuth(FeedMixin):
    template_name = 'feeds/artists/artists.html'
    model = ArtistProfile
    feedType = 'artists'
    default_order = "all"
    orders = {
        'latest': '-profile__user__date_joined',
        'all': None,
    }

class ArtistView (ArtistViewAuth, SignupEmailView, LoginView):
    pass

class AvailabilityView(AvailabilityMixin, ArtistViewAuth):
    template_name = 'feeds/artists/available.html'
    model = ArtistProfile

    def get_posts(self, **kwargs):
        # TODO: make properally timezone aware
        start = datetime.combine(self.start_date, time()).replace(tzinfo=utc)
        end = datetime.combine(self.end_date, time()).replace(tzinfo=utc)
        location = get_location(self.request, self.kwargs.get('zipcode'), 'point')
        if location:
            return self.model.objects.exclude(**self.get_exclude(start, end)).filter(
                Q(profile__user__calendar__events__line__line__distance_lte=(location, D(m=LocalFeed.distance))) |
                Q(profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance)))
            ).distinct()
        else:
            return []

available_artists = AvailabilityView.as_view()

class LocalViewAuth(ArtistViewAuth):

    def dispatch(self, *args, **kwargs):
        location = get_location(self.request, self.kwargs.get('zipcode'), 'point')
        if location:
            self.filters = {
                'profile__contact_info__location__zip_code__point__distance_lte': (location, D(m=LocalFeed.distance))
            }
        else:
            self.filters = {'profile__pk': -1}
        return super(LocalViewAuth, self).dispatch(*args, **kwargs)

class LocalView(LocalViewAuth, SignupEmailView, LoginView):
    pass

class FollowingView(ArtistViewAuth):
    template_name = 'feeds/artists/following.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        self.filters = {'profile__user__pk__in': self.request.user.following_set.values_list('target')}
        return super(FollowingView, self).dispatch(*args, **kwargs)

AUTH_VIEWS = {
    '50' : LocalViewAuth.as_view(),
    'following' : FollowingView.as_view(),
    'any-distance' : ArtistViewAuth.as_view(),
}

VIEWS = {
    '50' : LocalView.as_view(),
    'following' : FollowingView.as_view(),
    'any-distance' : ArtistView.as_view(),
}
