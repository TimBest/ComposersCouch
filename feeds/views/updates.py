from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import D
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from accounts.views import SignupEmailView, LoginView
from composersCouch.utils import get_page
from feeds.views import ZipcodeMixin
from feeds.utils import enrich_activities
from contact.utils import get_location
from feeds.models import Post
from feeds.post_feedly import feedly


"""from feedly.feed_managers.base import remove_operation
remove_operation(feed, activities)"""

login_required_m = method_decorator(login_required)

def updates(request, scope='any-distance', *args, **kwargs):
    kwargs['scope'] = scope
    if request.user.is_authenticated():
        views = AUTH_VIEWS
    else:
        views = VIEWS
    return views.get(scope, views['any-distance'])(request, *args, **kwargs)

class UpdateView(ZipcodeMixin, TemplateView):
    template_name = 'feeds/updates/local.html'
    feed = 'get_local_feed'
    location_type = 'code'
    feedType = 'updates'

    def get_scope(self, **kwargs):
        context = {}
        context['feedType'] = self.feedType
        context['scope'] = self.kwargs.get('scope', 'all')
        if context['scope'] == "any-distance":
            context['distance'] = "any distance"
        elif context['scope'] == "50":
            context['distance'] = "50 miles"
        return context

    def get_activities(self, page_num, zipcode, **kwargs):
        location = get_location(self.request, zipcode, self.location_type)
        if location:
            params = (location,)
            # TODO: paginate this feed
            feed = getattr(feedly, self.feed)(*params)
            activities = list(feed[:15])
            return enrich_activities(activities)
        return None

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context.update(self.get_scope())
        page_num = self.request.GET.get('page')
        zipcode = self.get_zipcode()
        context['activities'] = self.get_activities(page_num, zipcode)
        context['location'] = get_location(self.request, zipcode, 'code')
        return context

class LocalViewAuth(UpdateView):
    template_name = 'feeds/updates/local.html'
    feed = 'get_local_feed'
    location_type = 'code'

class LocalView(LocalViewAuth, SignupEmailView, LoginView):
    pass

class AllViewAuth(UpdateView):
    template_name = 'feeds/updates/all.html'

    def get_context_data(self, **kwargs):
        context = super(AllViewAuth, self).get_context_data(**kwargs)
        context.update(self.get_scope())
        page_num = self.request.GET.get('page')
        context['object_list'] = get_page(page_num, Post.objects.all().order_by('-created_at'), 15)
        return context

class AllView(AllViewAuth, SignupEmailView, LoginView):
    pass

class FollowingViewAuth(UpdateView):
    template_name='feeds/updates/following.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(FollowingViewAuth, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FollowingViewAuth, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        feed = feedly.get_feeds(self.request.user.id)['normal']
        activities = list(feed[:15])
        activities = get_page(page_num, activities, 15)
        context['activities'] = enrich_activities(activities)
        context['location'] = get_location(self.request, self.get_zipcode(), 'code')
        return context

class FollowingView(FollowingViewAuth, SignupEmailView, LoginView):
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
