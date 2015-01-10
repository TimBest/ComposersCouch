import mutagen
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from annoying.functions import get_object_or_None
from composersCouch.views import MultipleModelFormsView
from customProfile.views import ArtistProfileView, ProfileFormMixin
from photos.models import Image
from photos.forms import AlbumArtForm
from photos.views import ImageFormMixin
from tracks.forms import AlbumForm, AlbumAudioForm, TracksForm
from tracks.models import Album, Media, Track
from tracks.utils import json_playlist


class MusicView(ArtistProfileView):
    template_name = 'profile/musician/music.html'

music = MusicView.as_view()

class AlbumView(ImageFormMixin, MultipleModelFormsView):
    form_classes = {
      'albumForm' : AlbumForm,
      'albumArtForm' : AlbumArtForm
    }
    albumID=None
    template_name = 'profile/musician/forms/album.html'
    success_url = 'musician:tracksForm'

    def get_objects(self, queryset=None):
        self.albumID = self.kwargs.get('albumID', None)
        album = get_object_or_None(Album, id=self.albumID)
        return {
          'albumForm' : album,
          'albumArtForm' : album.album_art if album else None
        }

    def forms_valid(self, forms):
        album = forms['albumForm'].save(request=self.request, commit=False)
        album.musician_profile = self.request.user.profile.musicianProfile
        if self.request.FILES.get('image'):
            album.album_art = Image.objects.create(
                image=self.request.FILES.get('image'),
                title = album.title,
                user = self.request.user
            )
        elif self.request.POST.get('album_art'):
            imageId = self.request.POST.get('album_art')
            album.album_art = get_object_or_None(Image, id=imageId)
        album.save()
        forms['albumForm'].save(request=self.request)
        forms['albumForm'].save_m2m()
        return redirect(self.success_url, albumID=album.id)

AddEditAlbum = AlbumView.as_view()

class TracksView(ProfileFormMixin, UpdateView):
    form_class = AlbumAudioForm
    model = Album
    inline_model = Track
    object = None
    albumID = None
    template_name = 'profile/musician/forms/track.html'
    success_url = 'musician:music'

    def get_object(self, queryset=None):
        self.albumID = self.kwargs.get('albumID', None)
        album = get_object_or_None(self.model, id=self.albumID)
        self.object = album
        return album

    def get_formset(self):
        initial_list = []
        inline_formset = inlineformset_factory(self.model,
                                               self.inline_model,
                                               form=self.form_class,)
        form_kwargs = self.get_form_kwargs()
        formset = inline_formset(**form_kwargs)
        return formset

    def get_context_data(self):
        self.get_object()
        formset = self.get_formset()
        tracks = Track.objects.filter(album=self.albumID)
        formset_tracks = zip(formset, tracks)
        context = {
            'formset'        : formset,
            'formset_tracks' : formset_tracks,
            'tracks_form'    : TracksForm(**self.get_form_kwargs()),
            'media_url'      : settings.MEDIA_URL,
        }
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        context = self.get_context_data()
        if context['formset'].is_valid():
            context['formset'].save()
            if request.FILES.getlist('tracks'):
                context['tracks_form'].save(request=self.request)
                return redirect(request.path_info)
            else:
                return redirect(self.success_url, username=self.user.username)
        return render(request, self.template_name, context)

AddEditTracks = TracksView.as_view()
