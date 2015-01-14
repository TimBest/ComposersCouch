from django.conf.urls import include, patterns, url


urlpatterns = patterns('customProfile.views',
    url(r'^profile/edit/$', 'profile_edit', name='profile_edit'),
)
