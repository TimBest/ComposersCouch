from django.shortcuts import redirect
from django.views.generic import UpdateView

from annoying.functions import get_object_or_None
from contact.forms import MusicLinksForm, PhotoLinksForm, SocialLinksForm, VideoLinksForm
from contact.models import SocialLinks, MusicLinks
from customProfile.views import ProfileFormMixin


#Generic form for external link forms
class LinksView(ProfileFormMixin, UpdateView):
    model = SocialLinks

    def get_object(self, queryset=None):
        return get_object_or_None(self.model, profile=self.user.profile)

    def form_valid(self, form):
        social = form.save(commit=False)
        social.profile = self.user.profile
        social.save()
        return redirect(self.success_url, username=self.user.username)

#About page links to social media
class ArtistSocialView(LinksView):
    form_class = SocialLinksForm
    template_name = 'profile/forms/social_links.html'
    success_url = 'musician:about'
artist_social_links = ArtistSocialView.as_view()

class VenueSocialView(ArtistSocialView):
    success_url = 'venue:about'
venue_social_links = VenueSocialView.as_view()


#Photo page links to image sites
class ArtistPhotoView(LinksView):
    form_class = PhotoLinksForm
    template_name = 'profile/forms/photo_links.html'
    success_url = 'musician:photos'
artist_photo_links = ArtistPhotoView.as_view()

class VenuePhotoView(ArtistPhotoView):
    success_url = 'venue:photos'
venue_photo_links = VenuePhotoView.as_view()

#video page links to video sites
class ArtistVideoView(LinksView):
    form_class = VideoLinksForm
    template_name = 'profile/forms/video_links.html'
    success_url = 'musician:videos'
artist_video_links = ArtistVideoView.as_view()

class VenueVideoView(ArtistVideoView):
    success_url = 'venue:videos'
venue_video_links = VenueVideoView.as_view()


#music page links to music sites
class MusicLinksView(ProfileFormMixin, UpdateView):
    form_class = MusicLinksForm
    model = MusicLinks
    template_name = 'profile/forms/music_links.html'
    success_url = 'musician:music'

    def get_object(self, queryset=None):
        return get_object_or_None(self.model, profile=self.user.profile.musicianProfile)

    def form_valid(self, form):
        music = form.save(commit=False)
        music.profile = self.user.profile.musicianProfile
        music.save()
        return redirect(self.success_url, username=self.user.username)

music_links = MusicLinksView.as_view()
