from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, render, redirect, resolve_url
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.generic.base import View, TemplateView

from pipeline import create_profile
from forms import ClaimProfileForm, EmailForm, SignupForm, SigninForm
from models import Profile
from annoying.functions import get_object_or_None
from composersCouch.views import MultipleFormsView
from contact.forms import ZipcodeForm
from userena.signals import signup_complete
from userena.views import signin as userena_signin


login_required_m = method_decorator(login_required)

class SignupView(MultipleFormsView):
    template_name = 'accounts/signup/form.html'
    success_url = 'redirectToProfile'
    form_classes = {
      'signupForm'  : SignupForm,
      'zipcodeForm' : ZipcodeForm,
    }

    def forms_valid(self, forms):
        info = {}
        if forms.get('emailForm'):
            info['user'] = forms['emailForm'].save()
            info['password'] = forms['emailForm'].cleaned_data.get('password1')
        info['location'] = forms['zipcodeForm'].save()
        signupForm  = forms['signupForm']
        info['profile']  = signupForm.save(commit=False)
        info['first_name'] = signupForm.cleaned_data['first_name']
        info['last_name'] = signupForm.cleaned_data['last_name']
        info['band_name']  = signupForm.cleaned_data['band_name']
        info['venue_name'] = signupForm.cleaned_data['venue_name']
        return self.create_user_profile(info)

class SignupAuthView(SignupView):

    def dispatch(self, *args, **kwargs):
        username = self.kwargs.get('username', None)
        if self.request.user.is_authenticated():
            return redirect(self.request.user.profile.get_absolute_url())
        return super(SignupAuthView, self).dispatch(*args, **kwargs)

signup = SignupAuthView.as_view()

class SignupEmailView(SignupAuthView):
    template_name = 'accounts/signup/form_email.html'
    form_classes = {
      'signupForm'  : SignupForm,
      'zipcodeForm' : ZipcodeForm,
      'emailForm'   : EmailForm,
    }

    def create_user_profile(self, info):
        user = create_profile(
            info['user'], info['profile'].profile_type, info['location'],
            info['first_name'], info['last_name'], info['band_name'],
            info['venue_name'],
        )
        # A new signed user should logout the old one.
        if self.request.user.is_authenticated():
            logout(request)
        signup_complete.send(sender=None, user=user)
        user = authenticate(username=user.username, password=info['password'])
        login(self.request, user)
        return redirect(self.success_url, username=user.username)

signup_email = SignupEmailView.as_view()

class SignupSocialView(SignupAuthView):
    form_classes = {
      'signupForm'  : SignupForm,
      'zipcodeForm' : ZipcodeForm,
    }
    template_name = 'accounts/signup/form_social.html'

    def create_user_profile(self, info):
        self.request.session.update(info)
        backend = self.request.session.get('backend')
        return redirect('socialauth_complete', backend=backend)

signupSocial = SignupSocialView.as_view()

def claim_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    reset_form = PasswordResetForm({'email': profile.user.email})
    try:
        assert reset_form.is_valid()
        reset_form.save(
            domain_override="composerscouch.com",
            email_template_name='accounts/emails/profile_claim_message.txt',

        )
        return redirect('userena_password_reset_done')
    except:
        return redirect('claim_profile_error', username=username, error="error")

class VerifyProfileClaimView(TemplateView):
    template_name = 'accounts/signup/claim_profile.html'

    def get_context_data(self, **kwargs):
        username = kwargs.get('username')
        profile = get_object_or_404(Profile, user__username=username)
        return {
            'username': username,
            'profile' : profile,
            'error'   : kwargs.get('error')

        }
claim_profile_verify = VerifyProfileClaimView.as_view()

@sensitive_post_parameters()
@never_cache
def claim_profile_confirm(request, uidb64=None, token=None,
                           template_name='accounts/claim_profile_form.html',
                           token_generator=default_token_generator,
                           set_password_form=ClaimProfileForm,
                           post_reset_redirect='loginredirect',
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    assert uidb64 is not None and token is not None # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                user = form.save()
                user = authenticate(username=user.username, password=form.cleaned_data['new_password1'])
                login(request, user)
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    if current_app is not None:
        request.current_app = current_app
    return TemplateResponse(request, template_name, context)

def signin(request, auth_form=SigninForm,
           template_name='accounts/signin_form.html'):
    if request.user.is_authenticated():
        return redirect(request.user.profile)
    response = userena_signin(request, auth_form=auth_form,
                              template_name=template_name)
    return response

def loginredirect(request, username=None, tab='home'):
    if username == None:
        username = request.user.username
    profile = get_object_or_None(Profile, user__username=username)
    if profile:
        profileType = profile.profile_type
        if profileType == 'f':
          return redirect('fan:'+tab, username=username)
        elif profileType == 'm':
          return redirect('artist:'+tab, username=username)
        elif profileType == 'v':
          return redirect('venue:'+tab, username=username)
        return redirect(tab, username=username)
    else:
        return redirect('home')
