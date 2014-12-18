from customProfile.views import FanProfileView

class FanProfileView(FanProfileView):
    template_name = 'profile/fan/detail.html'

fan = FanProfileView.as_view()
