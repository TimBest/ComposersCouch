from datetime import date

from customProfile.views import ArtistProfileView, ProfileMixin, VenueProfileView


class ProfileShowsMixin(ProfileMixin):
    def get_context_data(self, **kwargs):
        context = super(ProfileShowsMixin, self).get_context_data(**kwargs)
        calendar = self.user.calendar
        year = self.request.GET.get('year')
        if year:
            events = calendar.get_yearly_events(int(year))
        else:
            events = calendar.get_recent()
            context['currentYear'] = year = date.today().year
        if self.user != self.request.user:
            context['events'] = events.filter(visible=True)
        else:
            context['events'] = events
        context['year'] = year
        return context

class ShowsView(ProfileShowsMixin, ArtistProfileView):
    template_name = 'profile/musician/shows.html'

shows = ShowsView.as_view()

class VenueProfileShowsView(ProfileShowsMixin, VenueProfileView):
    template_name = 'profile/venue/shows.html'

venue_shows = VenueProfileShowsView.as_view()
