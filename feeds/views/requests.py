from django.contrib.gis.measure import D
from django.utils import timezone
from django.views.generic import TemplateView

from contact.utils import get_location
from feeds.models import Follow
from feeds.post_feed import LocalFeed, RegionalFeed
from feeds.views import FeedMixin, GenreMixin
from request.models import PublicRequest


def requests(request, scope='all', *args, **kwargs):
    if scope == 'local':
        return LocalView.as_view()(request, *args, **kwargs)
    elif scope == 'regional':
        return ReqionalView.as_view()(request, *args, **kwargs)
    elif scope == 'following':
        return FollowingView.as_view()(request, *args, **kwargs)
    else:
        return AllView.as_view()(request, *args, **kwargs)

class RequestView(FeedMixin, TemplateView):
    modelManager = PublicRequest.objects
    path_to_genre = 'requester__profile__genre__slug'

    def band_or_venue(self, posts, **kwargs):
        if self.kwargs.get('for') == 'band':
            return posts.exclude(applicants__isnull=True)
        else:
            return posts.filter(applicants__isnull=True)
        return posts

    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs)
        context['for'] = self.get_for()
        return context

    def get_for(self):
        band_or_venue = self.kwargs.get('for')
        if band_or_venue == "band":
            return "band"
        elif band_or_venue == "venue":
            return "venue"
        else:
            if self.request.user.is_authenticated() and self.request.user.profile.profile_type == 'm':
                return "band"
            else:
                return "venue"

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

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        posts = self.modelManager.filter(
            zip_code__point__distance_lte=(location, D(m=LocalFeed.distance))
        )
        return self.band_or_venue(posts, **kwargs)

class ReqionalView(RequestView):
    template_name = 'feeds/requests/regional.html'

    def get_posts(self, **kwargs):
        location = get_location(self.request, self.get_zipcode(**kwargs), 'point')
        posts = self.modelManager.all()
        posts = self.modelManager.filter(
            zip_code__point__distance_lte=(location, D(m=RegionalFeed.distance))
        )
        return self.band_or_venue(posts, **kwargs)

class FollowingView(RequestView):
    template_name = 'feeds/requests/following.html'

    def get_posts(self, **kwargs):
        following = self.request.user.following_set.values_list('target')
        posts = self.modelManager.filter(
            requester__pk__in=following
        )
        return self.band_or_venue(posts, **kwargs)


class AllView(RequestView):
    template_name = 'feeds/requests/all.html'

    def get_posts(self, **kwargs):
        posts = self.modelManager.all()
        return self.band_or_venue(posts, **kwargs)
