from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import D
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import TemplateView

from composersCouch.utils import get_page
from feeds.views import FeedMixin, ZipcodeMixin
from feeds.utils import enrich_activities
from contact.utils import get_location
from feeds.models import Post
from feeds.post_feedly import feedly


"""from feedly.feed_managers.base import remove_operation
remove_operation(feed, activities)"""

def updates(request, scope='all', *args, **kwargs):
    if scope == 'local':
        return LocalView.as_view()(request, *args, **kwargs)
    elif scope == 'following':
        return FollowingView.as_view()(request, *args, **kwargs)
    else:
        return AllView.as_view()(request, *args, **kwargs)

class UpdateView(ZipcodeMixin, TemplateView):
    template_name = 'feeds/updates/local.html'
    feed = 'get_local_feed'
    location_type = 'code'

    def get_activities(self, page_num, zipcode, **kwargs):
        location = get_location(self.request, zipcode, self.location_type)
        if location:
            params = (location,)
            # TODO: paginate this feed
            feed = getattr(feedly, self.feed)(*params)
            activities = list(feed[:25])
            return enrich_activities(activities)
        return None

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        zipcode = self.get_zipcode()
        context['activities'] = self.get_activities(page_num, zipcode)
        context['location'] = get_location(self.request, zipcode, 'code')
        return context

class LocalView(UpdateView):
    template_name = 'feeds/updates/local.html'
    feed = 'get_local_feed'
    location_type = 'code'

class AllView(ZipcodeMixin, TemplateView):
    template_name = 'feeds/updates/all.html'
    path_to_genre = 'user__profile__genre__slug'

    def get_context_data(self, **kwargs):
        context = super(AllView, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        context['posts'] = get_page(page_num, Post.objects.all().order_by('-created_at'), 25)
        return context

class FollowingView(UpdateView):
    template_name='feeds/updates/following.html'

    def get_context_data(self, **kwargs):
        context = super(FollowingView, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        feed = feedly.get_feeds(self.request.user.id)['normal']
        activities = list(feed[:25])
        activities = get_page(page_num, activities, 25)
        context['activities'] = enrich_activities(activities)
        context['location'] = get_location(self.request, self.get_zipcode(), 'code')
        return context
