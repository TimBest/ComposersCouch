from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import D
from django.contrib.gis.geos import LineString
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.utils.timezone import utc

from accounts.views import SignupEmailView, LoginView
from composersCouch.utils import get_page
from contact.utils import get_location
from feeds.views import AvailabilityMixin, FeedMixin, GenreMixin
from feeds.post_feed import LocalFeed
from venue.models import VenueProfile


login_required_m = method_decorator(login_required)

def venues(request, scope='any-distance', *args, **kwargs):
    kwargs['scope'] = scope
    if request.user.is_authenticated():
        views = AUTH_VIEWS
    else:
        views = VIEWS
    return views.get(scope, views['any-distance'])(request, *args, **kwargs)

class VenueViewAuth(FeedMixin):
    model = VenueProfile
    feedType = 'venues'
    template_name = 'feeds/venues/venues.html'
    default_order = "all"
    orders = {
        'latest': '-profile__user__date_joined',
        'all': None,
    }

class VenueView(VenueViewAuth, SignupEmailView, LoginView):
    pass

class AvailabilityView(AvailabilityMixin, VenueViewAuth):
    template_name = 'feeds/venues/available.html'
    model = VenueProfile

    def get_posts(self, **kwargs):
        # TODO: add checking for when its more then a (x time period) away the default to local
        start = datetime.combine(self.start_date, time()).replace(tzinfo=utc)
        end = datetime.combine(self.end_date, time()).replace(tzinfo=utc)
        posts = self.model.objects.exclude(**self.get_exclude(start, end))
        location = get_location(self.request, self.kwargs.get('zipcode'), 'point')
        if location:
            return posts.filter(
                profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            ).distinct()
        else:
            return []

available_venues = AvailabilityView.as_view()

class BetweenView(AvailabilityView):
    template_name = 'feeds/venues/available_between.html'
    feedType = 'venues'

    def get_posts(self, **kwargs):
        # TODO: add checking for when its more then a (x time period) away the default to local
        start = datetime.combine(self.start_date, time()).replace(tzinfo=utc)
        end = datetime.combine(self.end_date, time()).replace(tzinfo=utc)
        posts = self.model.objects.exclude(**self.get_exclude(start, end))
        calendar = self.request.user.calendar
        prev = calendar.get_prev_event(in_datetime=end)
        next = calendar.get_next_event(in_datetime=end)
        if prev:
            start = prev.get_location().zip_code.point
        else:
            start = get_location(self.request, self.kwargs.get('zipcode'), 'point')
        if next:
            end = next.get_location().zip_code.point
        else:
            end = get_location(self.request, self.kwargs.get('zipcode'), 'point')
        line = LineString(start,end)
        return posts.filter(
            profile__contact_info__location__zip_code__point__distance_lte=(line, D(m=LocalFeed.distance))
        ).distinct()

available_venues_between = login_required(BetweenView.as_view())

class LocalViewAuth(VenueViewAuth):

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.kwargs.get('zipcode'), 'point')
        if location:
            return self.model.objects.filter(
                profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
        else:
            return []

class LocalView (LocalViewAuth, SignupEmailView, LoginView):
    pass

class FollowingView(VenueViewAuth):
    template_name = 'feeds/venues/following.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        self.filters = {'profile__user__pk__in': self.request.user.following_set.values_list('target')}
        return super(FollowingView, self).dispatch(*args, **kwargs)

AUTH_VIEWS = {
    '50' : LocalViewAuth.as_view(),
    'following' : FollowingView.as_view(),
    'any-distance' : VenueViewAuth.as_view(),
}

VIEWS = {
    '50' : LocalView.as_view(),
    'following' : FollowingView.as_view(),
    'any-distance' : VenueView.as_view(),
}
