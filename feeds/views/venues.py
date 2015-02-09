from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import D
from django.contrib.gis.geos import LineString
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.timezone import utc
from django.views.generic import TemplateView

from venue.models import VenueProfile
from composersCouch.utils import get_page
from contact.utils import get_location
from feeds.views import AvailabilityMixin, FeedMixin, GenreMixin
from feeds.post_feed import LocalFeed


def venues(request, scope='all', *args, **kwargs):
    if scope == 'local':
        return LocalView.as_view()(request, *args, **kwargs)
    elif scope == 'following':
        return FollowingView.as_view()(request, *args, **kwargs)
    else:
        return AllView.as_view()(request, *args, **kwargs)

class VenueView(FeedMixin, TemplateView):
    modelManager = VenueProfile.objects

    def get_default_order(self):
        return "all"

    def get_order(self, qs):
        order = self.kwargs.get('order')
        if order == "new":
            return qs.order_by('-profile__user__date_joined')
        else:
            # all
            return qs

class AvailabilityView(AvailabilityMixin, VenueView):
    template_name = 'feeds/venues/available.html'

    def get_posts(self, **kwargs):
        # TODO: add checking for when its more then a (x time period) away the default to local
        start = datetime.combine(self.start_date, time()).replace(tzinfo=utc)
        end = datetime.combine(self.end_date, time()).replace(tzinfo=utc)
        posts = self.modelManager.exclude(**self.get_exclude(start, end))
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if location:
            return posts.filter(
                profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
        else:
            return None

        if location:
            try:
                calendar = self.request.user.calendar
                prev = calendar.get_prev_event(in_datetime=end)
                next = calendar.get_next_event(in_datetime=end)
                if prev:
                    start = prev.get_location().zip_code.point
                else:
                    start = get_location(self.request, self.get_zipcode(**kwargs), 'point')
                if next:
                    end = next.get_location().zip_code.point
                else:
                    end = get_location(self.request, self.get_zipcode(**kwargs), 'point')
                line = LineString(start,end)
                return posts.filter(
                    profile__contact_info__location__zip_code__point__distance_lte=(line, D(m=LocalFeed.distance))
                )
            except:
                return posts.filter(
                    profile__user__calendar__events__line__line__distance_lte=(location, D(m=LocalFeed.distance))
                )
        else:
            return []

available_venues = AvailabilityView.as_view()

class BetweenView(AvailabilityView):
    template_name = 'feeds/venues/available_between.html'

    def get_posts(self, **kwargs):
        # TODO: add checking for when its more then a (x time period) away the default to local
        start = datetime.combine(self.start_date, time()).replace(tzinfo=utc)
        end = datetime.combine(self.end_date, time()).replace(tzinfo=utc)
        posts = self.modelManager.exclude(**self.get_exclude(start, end))
        calendar = self.request.user.calendar
        prev = calendar.get_prev_event(in_datetime=end)
        next = calendar.get_next_event(in_datetime=end)
        if prev:
            start = prev.get_location().zip_code.point
        else:
            start = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if next:
            end = next.get_location().zip_code.point
        else:
            end = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        line = LineString(start,end)
        return posts.filter(
            profile__contact_info__location__zip_code__point__distance_lte=(line, D(m=LocalFeed.distance))
        )

available_venues_between = AvailabilityView.as_view()

class LocalView(VenueView):
    template_name = 'feeds/venues/local.html'

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if location:
            return self.modelManager.filter(
                profile__contact_info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
        else:
            return []

class FollowingView(VenueView):
    template_name = 'feeds/venues/following.html'

    def get_posts(self, **kwargs):
        return self.modelManager.filter(
            profile__user__pk__in=self.request.user.following_set.values_list('target')
        )

class AllView(VenueView):
    template_name = 'feeds/venues/all.html'

    def get_posts(self, **kwargs):
        return self.modelManager.all()
