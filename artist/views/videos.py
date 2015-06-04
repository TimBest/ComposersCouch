from django.shortcuts import render, redirect

from customProfile.views import ArtistProfileView
from artist.views import TracksView
from tracks.forms import AlbumVideoForm


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
