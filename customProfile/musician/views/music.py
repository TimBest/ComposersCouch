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
from tracks.forms import AlbumForm, AlbumAudioForm
from tracks.models import Album, Media, Track
from tracks.utils import json_playlist


class MusicView(ArtistProfileView):
    template_name = 'profile/musician/music.html'

    def get_context_data(self, **kwargs):
        context = super(MusicView, self).get_context_data(**kwargs)
        musician_profile = context['musicianProfile']
        """if self.request.user == self.user:
            interviews = musician_profile.interviews.all()
        else:
            interviews = musician_profile.interviews.exclude(audio__isnull=True)
        context['interviews'] = json_playlist(tracks=interviews,
                                              viewname="musician:interview_form",
                                              username=context['username'])"""
        return context

music = MusicView.as_view()

def addTracksToAlbum(request, tracks, album):
    tracks_on_album = Track.objects.filter(album=album).count() + 1
    for file in tracks:
        try:
            file_path = file.temporary_file_path()
            metadata = mutagen.File(file_path, easy=True)
            if metadata and metadata.get('title'):
                title=metadata.get('title')[0]
        except:
            title = ""
        media = Media(audio=file, title=title)
        try:
            media.full_clean()
            media.set_upload_to_info(
                username=album.musician_profile.profile.user.username,
                track_type="albums",
                album_title=album.title
            )
            media.save()
            track = Track(media=media, order=tracks_on_album, album=album)
            tracks_on_album += 1
            track.save()
        except ValidationError as e:
            messages.error(request, e.messages[0]+" : "+str(file))

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
        forms['albumForm'].save_m2m()
        """addTracksToAlbum(self.request,
                         self.request.FILES.getlist('tracks'),
                         album)"""
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
        album = self.get_object()
        formset = self.get_formset()
        tracks = Track.objects.filter(album=self.albumID)
        formsetTracks = zip(formset, tracks)
        context = {
            'album'         : album,
            'formset'       : formset,
            'formsetTracks' : formsetTracks,
            'media_url'     : settings.MEDIA_URL,
        }
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        context = self.get_context_data()
        if context['formset'].is_valid():
            context['formset'].save()
            if not request.FILES.getlist('tracks'):
                return redirect(self.success_url, username=self.user.username)
            else:
                addTracksToAlbum(request,
                                 request.FILES.getlist('tracks'),
                                 context['album'])
                return redirect(request.path_info)
        return render(request, self.template_name, context)

AddEditTracks = TracksView.as_view()

"""class InterviewView(ProfileFormMixin, UpdateView):
    form_class = InterviewForm
    model = Interview
    trackID = None
    template_name = 'profile/musician/forms/interview.html'
    success_url = 'musician:music'

    def get_object(self, queryset=None):
        self.trackID = self.kwargs.get('trackID', None)
        track = get_object_or_None(self.model, id=self.trackID)
        return track

    def form_valid(self, form):
        track = form.save(commit=False)
        track.musician = self.user.profile.musicianProfile
        track.save()
        return redirect(self.success_url, username=self.user.username)

interview_form = InterviewView.as_view()
"""
