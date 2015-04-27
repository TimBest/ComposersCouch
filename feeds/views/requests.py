from django.contrib.gis.measure import D
from django.utils import timezone

from accounts.views import SignupEmailView, LoginView
from contact.utils import get_location
from feeds.post_feed import LocalFeed
from feeds.views import FeedMixin
from request.models import PublicRequest


def requests(request, scope='any-distance', *args, **kwargs):
    kwargs['scope'] = scope
    if request.user.is_authenticated():
        views = AUTH_VIEWS
    else:
        views = VIEWS
    return views.get(scope, views['any-distance'])(request, *args, **kwargs)

class RequestView(FeedMixin):
    model = PublicRequest
    path_to_genre = 'requester__profile__genre__slug'
    requests_for = 'artists'
    feedType = 'requests'
    default_order = "expiring"

    def dispatch(self, *args, **kwargs):
        self.requests_for = self.kwargs.get('for')
        return super(RequestView, self).dispatch(*args, **kwargs)

    def band_or_venue(self, posts, **kwargs):
        if self.requests_for == 'venue':
            return posts.filter(applicants__isnull=True)
        else:
            return posts.exclude(applicants__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs)
        context['for'] = self.requests_for
        return context

    def get_order(self, qs):
        order = self.kwargs.get('order')
        if qs:
            if order == "latest":
                return qs.order_by('-created_at').filter(fulfilled=False)
            else:
                #expiring
                return qs.order_by('accept_by').filter(accept_by__gte=timezone.now(), fulfilled=False)
        else:
            return qs

class LocalViewAuth(RequestView):
    template_name = 'feeds/requests/local.html'

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.kwargs.get('zipcode'), 'point')
        if location:
            posts = self.model.objects.filter(
                zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
            return self.band_or_venue(posts, **kwargs)
        else:
            return []

class LocalView(LocalViewAuth, SignupEmailView, LoginView):
    pass

class AllViewAuth(RequestView):
    template_name = 'feeds/requests/all.html'

    def get_posts(self, **kwargs):
        posts = self.model.objects.all()
        return self.band_or_venue(posts, **kwargs)

class AllView(AllViewAuth, SignupEmailView, LoginView):
    pass


AUTH_VIEWS = {
    '50' : LocalViewAuth.as_view(),
    'any-distance' : AllViewAuth.as_view(),
}

VIEWS = {
    '50' : LocalView.as_view(),
    'any-distance' : AllView.as_view(),
}
