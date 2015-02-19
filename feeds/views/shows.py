from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from contact.utils import get_location
from feeds.models import Follow
from feeds.post_feed import LocalFeed
from feeds.views import FeedMixin, GenreMixin
from schedule.models import Show


login_required_m = method_decorator(login_required)

def shows(request, scope='all', *args, **kwargs):
    kwargs['scope'] = scope
    if scope == 'local':
        return LocalView.as_view()(request, *args, **kwargs)
    elif scope == 'following':
        return FollowingView.as_view()(request, *args, **kwargs)
    else:
        return AllView.as_view()(request, *args, **kwargs)

class ShowView(FeedMixin, TemplateView):
    modelManager = Show.objects
    path_to_genre = 'info__venue__profile__genre__slug'
    # TODO: expand to also match with those preforming

    def get_default_order(self):
        return "upcoming"

    def get_posts(self, **kwargs):
        return self.modelManager.filter(visible=True)

    def get_order(self, qs):
        order = self.kwargs.get('order')
        if order == "new":
            return qs.order_by('-created_at')
        elif order == "all":
            return qs
        else:
            # Upcoming
            return qs.order_by('date__start').filter(date__start__gte=timezone.now())


class LocalView(ShowView):
    template_name = 'feeds/shows/local.html'

    def get_posts(self, **kwargs):
        posts = super(LocalView, self).get_posts(**kwargs)
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if location:
            return posts.filter(
                info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
        else:
            return []

class FollowingView(ShowView):
    template_name = 'feeds/shows/following.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(FollowingView, self).dispatch(*args, **kwargs)

    def get_posts(self,**kwargs):
        posts = super(FollowingView, self).get_posts(**kwargs)
        following = self.request.user.following_set.values_list('target')
        return posts.filter(
            Q(info__openers__profile__user__pk__in=following) | Q(info__headliner__profile__user__pk__in=following) | Q(info__venue__pk__in=following)
        )

class AllView(ShowView):
    template_name = 'feeds/shows/all.html'
