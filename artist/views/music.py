from django.conf import settings
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from annoying.functions import get_object_or_None
from annoying.views import MultipleModelFormsView
from customProfile.views import ArtistProfileView, ArtistProfileFormMixin
from photos.models import Image
from photos.forms import AlbumArtForm
from photos.views import ImageFormMixin
from tracks.forms import AlbumForm, AlbumAudioForm, TracksForm
from tracks.models import Album, Track


class MusicView(ArtistProfileView):
    template_name = 'artist/music.html'

music = MusicView.as_view()

class AlbumView(ArtistProfileFormMixin, ImageFormMixin, MultipleModelFormsView):
    form_classes = {
      'albumForm' : AlbumForm,
      'albumArtForm' : AlbumArtForm
    }
    album_id=None
    template_name = 'artist/forms/album.html'
    success_url = 'artist:tracksForm'

    def get_objects(self, queryset=None):
        self.album_id = self.kwargs.get('album_id', None)
        album = get_object_or_None(Album, id=self.album_id)
        return {
          'albumForm' : album,
          'albumArtForm' : album.album_art if album else None
        }

    def forms_valid(self, forms):
        album = forms['albumForm'].save(request=self.request, commit=False)
        album.artist_profile = self.request.user.profile.artist_profile
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
        return redirect(self.success_url, album_id=album.id)

AddEditAlbum = AlbumView.as_view()

class TracksView(ArtistProfileFormMixin, UpdateView):
    form_class = AlbumAudioForm
    model = Album
    inline_model = Track
    object = None
    album_id = None
    template_name = 'artist/forms/track.html'
    success_url = 'artist:music'

    def get_object(self, queryset=None):
        self.album_id = self.kwargs.get('album_id', None)
        album = get_object_or_None(self.model, id=self.album_id)
        self.object = album
        return album

    def get_formset(self):
        inline_formset = inlineformset_factory(self.model,
                                               self.inline_model,
                                               form=self.form_class,)
        form_kwargs = self.get_form_kwargs()
        formset = inline_formset(**form_kwargs)
        return formset

    def get_context_data(self):
        self.get_object()
        formset = self.get_formset()
        tracks = Track.objects.filter(album=self.album_id)
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
            for form in context['formset']:
                cleaned_data = form.cleaned_data
                if cleaned_data:
                    track = cleaned_data['id']
                    track.title = cleaned_data['title']
                    track.save()
                    form.save()
            if request.FILES.getlist('tracks'):
                context['tracks_form'].save(request=self.request)
                return redirect(request.path_info)
            else:
                return redirect(self.success_url, username=self.user.username)
        return render(request, self.template_name, context)

AddEditTracks = TracksView.as_view()
