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

urlpatterns += patterns('annoying.views',
    url(r'^tour/$', 'load_template', {'template_name': 'tour.html'}, name='tour'),

    # Footer
    url(r'^about/$', 'load_template', {'template_name': 'footer/about.html'}, name='about'),
    url(r'^team/$', 'load_template', {'template_name': 'footer/team.html'}, name='team'),
    url(r'^credit/$', 'load_template', {'template_name': 'footer/credit.html'}, name='credit'),
)
urlpatterns += patterns('composersCouch.views',
    # Landing Page
    url(r'^$', 'landing_page', name='home'),
)

urlpatterns += patterns('',
    url(r'^a/', include('artist.urls', namespace='artist')),
    url(r'^f/', include('fan.urls', namespace='fan')),
    url(r'^v/', include('venue.urls', namespace='venue')),
)

urlpatterns += patterns('',
    url(r'', include('accounts.urls')),
    url(r'', include('customProfile.urls')),
    url(r'', include('feeds.urls')),
    url(r'', include('request.urls')),
    url(r'', include('schedule.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^inbox/', include('threads.urls', namespace='threads')),
    url(r'^photos/', include('photos.urls', namespace='photos')),
    url(r'^progressbarupload/', include('progressbarupload.urls')),
    # TODO/WARNING: hard coded in base.js
    url(r'^search/', include('search.urls')),
)

if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        # TODO/WARNING: media url is hard coded in auto complete templates
        url(r'^media/(?P<path>.*)$','django.views.static.serve',
            {'document_root':  getattr(settings, 'MEDIA_ROOT', '/media')}),
    )
