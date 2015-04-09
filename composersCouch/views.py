from django.views.generic.base import TemplateView

from accounts.views import SignupEmailView, LoginView
from feeds.views import ShowView


class LandingPage(SignupEmailView, LoginView, ShowView):
    template_name = "landing_page.html"

landing_page = LandingPage.as_view()
