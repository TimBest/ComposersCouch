from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, FormView

from guardian.decorators import permission_required_or_403

from customProfile import forms as profile_forms
from accounts.models import FanProfile, MusicianProfile, VenueProfile, Profile
from annoying.functions import get_object_or_None
from composersCouch.views import MultipleFormsView
from composersCouch.utils import get_page
from feeds.models import Follow, Post
from photos.models import Image
from photos.forms import MugshotForm
from photos.views import ImageFormMixin

from django.utils.decorators import method_decorator


class ProfileMixin(object):

    def dispatch(self, *args, **kwargs):
        username = self.kwargs.get('username')
        self.user = get_object_or_404(User, username=username)
        return super(ProfileMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileMixin, self).get_context_data(**kwargs)
        context['username'] = self.user.username
        context['profile'] = self.user.profile
        context['media_url'] = settings.MEDIA_URL
        if self.request.user == self.user:
            context['isEditable'] = 'visible'
        else:
            context['isEditable'] = 'hidden'
        follows = get_object_or_None(Follow, user=self.request.user.id,
                                     target=self.user.id)
        if follows:
            context['isFollowing'] = 'isFollowing'
        return context

class ProfileFormMixin(object):
    #@method_decorator(permission_required_or_403('change_profile', (Profile, 'user__username', 'username',)))
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super(ProfileFormMixin, self).dispatch(*args, **kwargs)

def profileRedirect(request, username, redirect_url):
    return redirect(redirect_url, username=username)

class FanProfileView(ProfileMixin, TemplateView):
    template_name = 'profile/fan/news.html'

    def get_context_data(self, **kwargs):
        context = super(FanProfileView, self).get_context_data(**kwargs)
        context['fanProfile'] = context['profile'].fanProfile
        return context

class ArtistProfileView(ProfileMixin, TemplateView):
    template_name = 'profile/musician/news.html'

    def get_context_data(self, **kwargs):
        context = super(ArtistProfileView, self).get_context_data(**kwargs)
        context['musicianProfile'] = context['profile'].musicianProfile
        return context

class VenueProfileView(ProfileMixin, TemplateView):
    template_name = 'profile/fan/news.html'

    def get_context_data(self, **kwargs):
        context = super(VenueProfileView, self).get_context_data(**kwargs)
        context['venueProfile'] = context['profile'].venueProfile
        return context

class ProfileEdit(ImageFormMixin, MultipleFormsView):
    template_name = 'profile/forms/edit_profile.html',
    success_url = 'redirectToProfile'

    def get_forms(self):
        forms = {}
        user = self.request.user
        form_kwargs = self.get_form_kwargs()
        forms['usernameForm'] = profile_forms.UsernameForm(instance=user, **form_kwargs)
        forms['mugshotFrom'] = MugshotForm(instance=user.profile.mugshot, **form_kwargs)
        forms['profileForm'] = profile_forms.ProfileForm(instance=user.profile, **form_kwargs)
        profile_type = user.profile.profile_type
        if profile_type == 'f':
            forms['typedForm'] = profile_forms.UserForm(instance=user, **form_kwargs)
        elif profile_type == 'm':
            forms['typedForm'] = profile_forms.MusicianProfileForm(instance=user.profile.musicianProfile, **form_kwargs)
        elif profile_type == 'v':
            forms['typedForm'] = profile_forms.VenueProfileForm(instance=user.profile.venueProfile, **form_kwargs)
        return forms

    def forms_valid(self, forms):
        forms['typedForm'].save()
        user = forms['usernameForm'].save()
        username = user.username
        user.calendar.slug = user.calendar.name = username
        user.calendar.save()
        profile = forms['profileForm'].save()
        if self.request.FILES.get('image'):
            profile.mugshot = Image.objects.create(
                image=self.request.FILES.get('image'),
                title = "Mugshot",
                user = user
            )
        elif self.request.POST.get('mugshot'):
            imageId = self.request.POST.get('mugshot')
            profile.mugshot = get_object_or_None(Image, id=imageId)
        profile.save()
        return redirect(self.success_url, username=username)

profile_edit = login_required(ProfileEdit.as_view())
