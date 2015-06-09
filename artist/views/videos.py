from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.views.generic import FormView

from customProfile.views import ArtistProfileView, ArtistProfileFormMixin
from artist.views import TracksView
from tracks.forms import AlbumVideoForm, VideoForm
from tracks.models import Video


class VideoView(ArtistProfileView):
    template_name = 'artist/videos.html'

videos = VideoView.as_view()

class TrackVideoView(TracksView):
    form_class = AlbumVideoForm
    template_name = 'artist/forms/track_video.html'
    success_url = 'artist:videos'

    def get_context_data(self):
        return {
            'album'  : self.get_object(),
            'formset': self.get_formset(),
        }

    def post(self, request, **kwargs):
        context = self.get_context_data()
        #print context
        if context['formset'].is_valid():
            context['formset'].save()
            #for form in context['formset']:
            #    form.save()
            return redirect(self.success_url, username=self.user.username)
        else:
            return render(request, self.template_name, context)

add_video_to_album = TrackVideoView.as_view()

class VideoFormView(ArtistProfileFormMixin, FormView):
    template_name = 'artist/forms/videos.html'
    model = Video
    form_class = VideoForm
    success_url = 'artist:videos'
    extra = 3

    def get_form(self, form_class=None):
        formset = modelformset_factory(self.model, self.form_class, extra=self.extra, exclude=('',))
        videos = self.model.objects.filter(user=self.user)
        form_kwargs = self.get_form_kwargs()
        return formset(queryset=videos, **form_kwargs)

    def form_valid(self, form):
      for f in form:
        if f.has_changed():
            video = f.save(commit=False)
            if video:
                video.user = self.user
                video.save()
      return redirect(self.success_url, username=self.user.username)

video_form = VideoFormView.as_view()
