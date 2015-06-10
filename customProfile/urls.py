from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('customProfile.views',
    url(r'^profile/edit/$', 'profile_edit', name='profile_edit'),
)
