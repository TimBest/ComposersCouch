import autocomplete_light
from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap

from accounts.sitemap import AuthViewSitemap
from artist.sitemap import ArtistSitemap
from composersCouch.sitemap import StaticViewSitemap
from fan.sitemap import FanSitemap
from feeds.sitemap import FeedsSitemap
from schedule.sitemap import ShowSitemap
from venue.sitemap import VenueSitemap


sitemaps = {
    'artists': ArtistSitemap(),
    'auth': AuthViewSitemap(),
    'fans': FanSitemap(),
    'feeds': FeedsSitemap(),
    'shows': ShowSitemap(),
    'static': StaticViewSitemap(),
    'venues': VenueSitemap(),
}

autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^robots.txt$', include('robots.urls')),
)

urlpatterns += patterns('annoying.views',
    url(r'^learn/$', 'load_template', {'template_name': 'static/learn.html'}, name='learn'),
    url(r'^changelog/$', 'load_template', {'template_name': 'static/changelog.html'}, name='changelog'),
    url(r'^pipeline/$', 'load_template', {'template_name': 'static/pipeline.html'}, name='pipeline'),

    # Footer
    url(r'^about/$', 'load_template', {'template_name': 'static/about.html'}, name='about'),
    url(r'^team/$', 'load_template', {'template_name': 'static/team.html'}, name='team'),
    url(r'^credit/$', 'load_template', {'template_name': 'static/credit.html'}, name='credit'),
)
urlpatterns += patterns('feeds.views',
    # Landing Page
    url(r'^$', 'shows', name='home'),
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
