import autocomplete_light
from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('composersCouch.views',
    url(r'^$',
        'home',
        name='home'),
    url(r'^team/$',
        'load_template',
        {'template_name': 'footer/team.html'},
        name='team'),
    url(r'^credit/$',
        'load_template',
        {'template_name': 'footer/credit.html'},
        name='credit'),
    url(r'^colorScheme/$',
        'load_template',
        {'template_name': 'footer/colors.html'},
        name='colors'),
)

urlpatterns += patterns('',
    url(r'^f/', include('customProfile.fan.urls', namespace='fan')),
    url(r'^m/', include('customProfile.musician.urls', namespace='musician')),
    url(r'^v/', include('customProfile.venue.urls', namespace='venue')),
)

urlpatterns += patterns('',
    url(r'', include('accounts.urls')),
    url(r'', include('customProfile.urls')),
    url(r'', include('feeds.urls')),
    url(r'^', include('request.urls')),
    url(r'', include('schedule.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^gallery/', include('photos.urls', namespace='photos')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # WARNING/TODO: media url is hard coded in auto complete templates
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
        {'document_root':  getattr(settings, 'MEDIA_ROOT', '/media')}),
    url(r'^messages/', include('threaded_messages.urls')),
    url(r'^progressbarupload/', include('progressbarupload.urls')),
    url(r'^search', include('search.urls')),
)
