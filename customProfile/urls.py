from django.conf.urls import include, patterns, url


urlpatterns = patterns('customProfile.views',
    url(r'^(?P<username>[-\w]+)/editProfile/$',
        'profile_edit',
        name='profile_edit'),
)
