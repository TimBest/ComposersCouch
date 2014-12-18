from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import FormView

from composersCouch.views import MultipleFormsView
from customProfile.views import ProfileMixin
from feeds.forms import PostForm
from feeds.post_feedly import feedly
from feeds.utils import enrich_activities
from annoying.functions import get_object_or_None
from photos.forms import ImageOnlyForm
from photos.models import Image
from photos.views import ImageFormMixin


class ProfileNewsMixin(ProfileMixin, ImageFormMixin, MultipleFormsView):
    form_classes = {
        'post_form' : PostForm,
        'photo_form' : ImageOnlyForm
    }

    def get_context_data(self, **kwargs):
        context = super(ProfileNewsMixin, self).get_context_data(**kwargs)
        feed = feedly.get_user_feed(self.user.id)
        activities = list(feed[:25])
        context['activities'] = enrich_activities(activities)
        return context

    def forms_valid(self, forms):
        post = forms['post_form'].save(commit=False)
        username = self.kwargs.get('username')
        target = get_object_or_None(User, username=username)
        post = feedly.create_and_add_post(
            user=self.request.user,
            target=target,
            title=post.title,
            message=post.message
        )
        if self.request.FILES.get('image'):
            image = Image.objects.create(
                image=self.request.FILES.get('image'),
                title = post.title,
                user = self.request.user
            )
            post.photo = image
        elif self.request.POST.get('photo'):
            imageId = self.request.POST.get('photo')
            image = get_object_or_None(Image, id=imageId)
            post.photo = image
        post.save()
        return redirect(self.success_url, username=username)


class ArtistNewsView(ProfileNewsMixin):
    template_name = 'profile/musician/news.html'
    success_url = 'musician:news'

    def get_context_data(self, **kwargs):
        context = super(ArtistNewsView, self).get_context_data(**kwargs)
        context['musicianProfile'] = context['profile'].musicianProfile
        return context

artist_news = ArtistNewsView.as_view()

class FanNewsView(ProfileNewsMixin):
    template_name = 'profile/fan/news.html'
    success_url = 'fan:news'

    def get_context_data(self, **kwargs):
        context = super(FanNewsView, self).get_context_data(**kwargs)
        context['fanProfile'] = context['profile'].fanProfile
        return context

fan_news = FanNewsView.as_view()

class VenueNewsView(ProfileNewsMixin):
    template_name = 'profile/venue/news.html'
    success_url = 'venue:news'

    def get_context_data(self, **kwargs):
        context = super(VenueNewsView, self).get_context_data(**kwargs)
        context['venueProfile'] = context['profile'].venueProfile
        return context

venue_news = VenueNewsView.as_view()
