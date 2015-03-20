from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import D
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from contact.utils import get_location
from feeds.models import Follow
from feeds.post_feed import LocalFeed
from feeds.views import FeedMixin, GenreMixin
from request.models import PublicRequest


login_required_m = method_decorator(login_required)

def requests(request, scope='any-distance', *args, **kwargs):
    kwargs['scope'] = scope
    if scope == '50':
        return LocalView.as_view()(request, *args, **kwargs)
    else:
        return AllView.as_view()(request, *args, **kwargs)

class RequestView(FeedMixin, TemplateView):
    modelManager = PublicRequest.objects
    path_to_genre = 'requester__profile__genre__slug'
    requests_for = 'band'

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

    def get_default_order(self):
        return "expiring"

    def get_order(self, qs):
        order = self.kwargs.get('order')
        if order == "new":
            return qs.order_by('-created_at').filter(fulfilled=False)
        elif order == "all":
            return qs
        else:
            #expiring
            return qs.order_by('accept_by').filter(accept_by__gte=timezone.now(), fulfilled=False)

class LocalView(RequestView):
    template_name = 'feeds/requests/local.html'

    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs)
        context['distance'] = "50 miles"
        return context

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        if location:
            posts = self.modelManager.filter(
                zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
            )
            return self.band_or_venue(posts, **kwargs)
        else:
            return []

class AllView(RequestView):
    template_name = 'feeds/requests/all.html'

    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs)
        context['distance'] = "any distance"
        return context

    def get_posts(self, **kwargs):
        posts = self.modelManager.all()
        return self.band_or_venue(posts, **kwargs)
