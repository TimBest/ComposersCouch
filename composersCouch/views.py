from django.views.generic.base import TemplateView

from accounts.views import SignupEmailView, LoginView
from feeds.views import ShowView



def landing_page(request, *args, **kwargs):
    if request.user.is_authenticated():
        return LandingPageAuthenticated.as_view()(request, *args, **kwargs)
    else:
        return LandingPage.as_view()(request, *args, **kwargs)

class LandingPage(SignupEmailView, LoginView, ShowView):
    template_name = "landing_page.html"

class LandingPageAuthenticated(ShowView):
    template_name = "landing_page.html"
