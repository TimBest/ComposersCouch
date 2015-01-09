from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView

from guardian.decorators import permission_required_or_403
from userena import views as userena_views

from pipeline import create_profile
from forms import CreateUserForm, EmailForm, SignupForm, SigninForm
from models import Profile
from composersCouch.views import MultipleFormsView
from contact.forms import ZipcodeForm
from userena import signals as userena_signals


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
        info['location'] = forms['zipcodeForm'].save()
        info['email'] = forms['zipcodeForm'].cleaned_data.get('email')
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
            return redirect('redirectToProfile',
                            username = self.request.user.username)
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
        userena_signals.signup_complete.send(sender=None,
                                             user=user)
        user = authenticate(identification=user.email, check_password=False)
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

class SignupNoOwnerView(SignupView):
    template_name = 'accounts/signup/form_no_owner.html'
    success_url = 'home'
    form_classes = {
      'signupForm'  : SignupForm,
      'zipcodeForm' : CreateUserForm,
    }

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(SignupNoOwnerView, self).dispatch(*args, **kwargs)

    def create_user_profile(self, info):
        user = User.objects.create_user(username=get_random_string(),
                                        email=info['email'])
        # apparently django does not let you reset a password if one is not initally set
        user.set_password(get_random_string())
        user.save
        info['profile'].user = user
        info['profile'].has_owner = False
        info['profile'].save()
        location = self.request.user.profile.contact_info.location
        location.pk = None
        location.save()
        user = create_profile(
            user, info['profile'].profile_type, location,
            info['first_name'], info['last_name'], info['band_name'],
            info['venue_name'],
        )
        return redirect(self.success_url)

signupNoOwner = SignupNoOwnerView.as_view()

def claim_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    reset_form = PasswordResetForm({'email': profile.user.email})
    try:
        assert reset_form.is_valid()
        reset_form.save(
            email_template_name='accounts/emails/password_reset_message.txt',
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

def signin(request, auth_form=SigninForm,
           template_name='accounts/signin_form.html'):
    if request.user.is_authenticated():
        return redirect('redirectToProfile',
                        username = request.user.username)

    response = userena_views.signin(request, auth_form=auth_form,
                                    template_name=template_name)

    return response

def loginredirect(request, username=None,tab='home'):
    if username == None:
        username = request.user.username
    profile = get_object_or_404(Profile, user__username=username)
    profileType = profile.profile_type
    if profileType == 'f':
      return redirect('fan:'+tab, username=username)
    elif profileType == 'm':
      return redirect('musician:'+tab, username=username)
    elif profileType == 'v':
      return redirect('venue:'+tab, username=username)
    return redirect(tab, username=username)
