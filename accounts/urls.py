from django.conf.urls import include, patterns, url
from django.contrib.auth.views import password_reset_confirm

from userena.compat import auth_views_compat_quirks, password_reset_uid_kwarg
from userena.urls import merged_dict


urlpatterns = patterns('accounts.views',
    url(r'^signin/$', 'signin', name='signin'),
    url(r'^signup/$', 'signup', {'template_name': 'accounts/signup/form.html'}, name='signup'),
    url(r'^signup/email/$', 'signup_email', name='signup_email'),
    # url is hard coded in getProfileDetails() in accounts.pipeline.py
    url(r'^signup/social/$', 'signupSocial', name='signupSocial'),
    url(r'^signup/complete/(?P<username>[-\w]+)$', 'loginredirect',  name='userena_signup_complete'),

    url(r'^loginredirect/$', 'loginredirect', name='loginredirect'),
    url(r'^redirect/(?P<username>[-\w]+)/$', 'loginredirect', name='redirectToProfile'),
    url(r'^redirect/(?P<username>[-\w]+)/(?P<tab>[-\w]+)$', 'loginredirect', name='redirectToProfile'),

    url(r'^claim/profile/(?P<username>[-\w]+)$', 'claim_profile', name='claim_profile'),
    url(r'^verify/profile/claim/(?P<username>[-\w]+)$', 'claim_profile_verify', name='claim_profile_verify'),
    url(r'^verify/profile/claim/(?P<username>[-\w]+)/(?P<error>[-\w]+)$', 'claim_profile_verify', name='claim_profile_error'),
    url(r'^confirm/profile/claim/(?P<%s>[0-9A-Za-z]+)-(?P<token>.+)/$' % password_reset_uid_kwarg,
       password_reset_confirm,
       merged_dict({'template_name': 'accounts/password_reset_confirm_form.html',
                    }, auth_views_compat_quirks['userena_password_reset_confirm']),
       name='confirm_profile_claim'),
)
