from customProfile.views import FanProfileView

class FanProfileView(FanProfileView):
    template_name = 'fan/detail.html'

fan = FanProfileView.as_view()
