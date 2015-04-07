from django.views.generic.base import TemplateView

from feeds.views import ShowView


class LandingPage(ShowView):
    template_name = "landing_page.html"

landing_page = LandingPage.as_view()
