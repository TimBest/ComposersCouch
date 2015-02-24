from django.shortcuts import redirect
from django.views.generic import UpdateView

from annoying.functions import get_object_or_None
from customProfile.views import ArtistProfileFormMixin, VenueProfileFormMixin
from social_links.forms import MusicLinksForm, PhotoLinksForm, SocialLinksForm, VideoLinksForm
from social_links.models import SocialLinks, MusicLinks


#Generic form for external link forms
class LinksView(UpdateView):
    model = SocialLinks

    def get_object(self, queryset=None):
        return get_object_or_None(self.model, profile=self.user.profile)

    def form_valid(self, form):
        social = form.save(commit=False)
        social.profile = self.user.profile
        social.save()
        return redirect(self.success_url, username=self.user.username)

#About page links to social media
class ArtistSocialView(ArtistProfileFormMixin, LinksView):
    form_class = SocialLinksForm
    template_name = 'profile/forms/social_links.html'
    success_url = 'artist:about'
artist_social_links = ArtistSocialView.as_view()

class VenueSocialView(VenueProfileFormMixin, LinksView):
    form_class = SocialLinksForm
    template_name = 'profile/forms/social_links.html'
    success_url = 'venue:about'
venue_social_links = VenueSocialView.as_view()


#Photo page links to image sites
class ArtistPhotoView(ArtistProfileFormMixin, LinksView):
    form_class = PhotoLinksForm
    template_name = 'profile/forms/photo_links.html'
    success_url = 'artist:photos'
artist_photo_links = ArtistPhotoView.as_view()

class VenuePhotoView(VenueProfileFormMixin, LinksView):
    form_class = PhotoLinksForm
    template_name = 'profile/forms/photo_links.html'
    success_url = 'venue:photos'
venue_photo_links = VenuePhotoView.as_view()


#video page links to video sites
class ArtistVideoView(ArtistProfileFormMixin, LinksView):
    form_class = VideoLinksForm
    template_name = 'profile/forms/video_links.html'
    success_url = 'artist:videos'
artist_video_links = ArtistVideoView.as_view()

class VenueVideoView(VenueProfileFormMixin, LinksView):
    form_class = VideoLinksForm
    template_name = 'profile/forms/video_links.html'
    success_url = 'venue:videos'
venue_video_links = VenueVideoView.as_view()


#music page links to music sites
class MusicLinksView(ArtistProfileFormMixin, UpdateView):
    form_class = MusicLinksForm
    model = MusicLinks
    template_name = 'profile/forms/music_links.html'
    success_url = 'artist:music'

    def get_object(self, queryset=None):
        return get_object_or_None(self.model, profile=self.user.profile.artist_profile)

    def form_valid(self, form):
        music = form.save(commit=False)
        music.profile = self.user.profile.artist_profile
        music.save()
        return redirect(self.success_url, username=self.user.username)

music_links = MusicLinksView.as_view()
