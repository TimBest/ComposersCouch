from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.utils.decorators import method_decorator

from accounts.views import SignupEmailView, LoginView
from contact.utils import get_location
from feeds.models import Follow
from feeds.post_feed import LocalFeed
from feeds.views import FeedMixin, GenreMixin
from schedule.models import Show


login_required_m = method_decorator(login_required)

def shows(request, scope='any-distance', *args, **kwargs):
    kwargs['scope'] = scope
    if request.user.is_authenticated():
        views = AUTH_VIEWS
    else:
        views = VIEWS
    return views.get(scope, views['any-distance'])(request, *args, **kwargs)

class ShowViewAuth(FeedMixin):
    model = Show
    path_to_genre = 'info__venue__profile__genre__slug'
    template_name = 'feeds/shows/shows.html'
    feedType = 'shows'
    default_order = "upcoming"
    # TODO: expand to also match with those preforming

    def get_posts(self, **kwargs):
        return self.model.objects.filter(visible=True)

    def get_order(self, qs):
        order = self.kwargs.get('order')
        if order == "latest":
            return qs.order_by('-created_at')
        elif order == "all":
            return qs
        else:
            # Upcoming
            return qs.order_by('date__start').filter(date__start__gte=timezone.now())

class ShowView (ShowViewAuth, SignupEmailView, LoginView):
    pass

class LocalViewAuth(ShowViewAuth):

    def get_posts(self, **kwargs):
        posts = super(LocalViewAuth, self).get_posts(**kwargs)
        location = get_location(self.request, self.kwargs.get('zipcode'), 'point')
        if location:
            return posts.filter(
                info__location__zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
        else:
            return []

class LocalView(LocalViewAuth, SignupEmailView, LoginView):
    pass

class FollowingView(ShowViewAuth):
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

AUTH_VIEWS = {
    '50' : LocalViewAuth.as_view(),
    'following' : FollowingView.as_view(),
    'any-distance' : ShowViewAuth.as_view(),
}

VIEWS = {
    '50' : LocalView.as_view(),
    'following' : FollowingView.as_view(),
    'any-distance' : ShowView.as_view(),
}
