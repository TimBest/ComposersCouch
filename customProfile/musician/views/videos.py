from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from annoying.functions import get_object_or_None
from customProfile.views import ArtistProfileView, ProfileFormMixin
from customProfile.musician.views import TracksView
from tracks.forms import AlbumVideoForm#, LiveVideoForm, InterviewVideoForm
from tracks.models import Album, Interview, Media


class VideoView(ArtistProfileView):
    template_name = 'profile/musician/videos.html'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        musician_profile = context['musicianProfile']
        """
        if self.request.user == self.user:
            context['interviews'] = musician_profile.interviews.all()
        else:
            context['interviews'] = musician_profile.interviews.exclude(video__isnull=True)
        """
        return context

videos = VideoView.as_view()

class TrackVideoView(TracksView):
    form_class = AlbumVideoForm
    template_name = 'profile/musician/forms/track_video.html'
    success_url = 'musician:videos'

    def get_context_data(self):
        return {
            'album'  : self.get_object(),
            'formset': self.get_formset(),
        }

    def post(self, request, username, **kwargs):
        context = self.get_context_data()
        if context['formset'].is_valid():
            context['formset'].save()
            return redirect(self.success_url, username=username)
        return render(request, self.template_name, context)

add_video_to_album = TrackVideoView.as_view()

"""class LiveVideoView(LiveTrackView):
    form_class = LiveVideoForm
    template_name = 'profile/musician/forms/live_video.html'
    success_url = 'musician:videos'

live_video_form = LiveVideoView.as_view()

class InterviewView(LiveVideoView):
    form_class = InterviewVideoForm
    model = Interview
    template_name = 'profile/musician/forms/interview_video.html'
    success_url = 'musician:videos'

interview_video_form = InterviewView.as_view()"""