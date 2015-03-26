from django.conf.urls import include, patterns, url


view_location = 'feeds.views'

# used in feed system for redirect when appending zipcode onto url
homeCategory = 'requests'
homeScope = 'all'

urlpatterns = patterns(view_location,
    url(r'^follow/$', 'follow', name='follow'),
    url(r'^remove_post/$', 'remove_post', name='remove_post'),
    url(r'^zipcode/$', 'zipcode', name='zipcode'),
    url(r'^genre/$', 'genre', name='genre'),
    url(r'^availability/$', 'availability', name='availability'),

    url(r'^(?P<order>[-\w]+)/', include(patterns(view_location,
        url(r'^artists/(?P<scope>[-\w]+)/$', 'artists', name='artists'),
        url(r'^artists/(?P<scope>[-\w]+)/(?P<zipcode>[-\w]+)/$', 'artists', name='artists'),
        url(r'artist/availability/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/', include(patterns(view_location,
            url(r'^$', 'available_artists', name='available_artists'),
            url(r'^(?P<zipcode>[-\w]+)/$', 'available_artists', name='available_artists'),
        ))),

        url(r'^requests/(?P<for>[-\w]+)/(?P<scope>[-\w]+)/$','requests',name='requests'),
        url(r'^requests/(?P<for>[-\w]+)/(?P<scope>[-\w]+)/(?P<zipcode>[-\w]+)/$', 'requests', name='requests'),

        url(r'^shows/(?P<scope>[-\w]+)/$', 'shows', name='shows'),
        url(r'^shows/(?P<scope>[-\w]+)/(?P<zipcode>[-\w]+)/$', 'shows', name='shows'),

        url(r'^venues/(?P<scope>[-\w]+)/$', 'venues', name='venues'),
        url(r'^venues/(?P<scope>[-\w]+)/(?P<zipcode>[-\w]+)/$', 'venues', name='venues'),
        url(r'venue/availability/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/', include(patterns(view_location,
            url(r'^$', 'available_venues', name='available_venues'),
            url(r'^inbetween/$', 'available_venues_between', name='available_venues_between'),
            url(r'^(?P<zipcode>[-\w]+)/$', 'available_venues', name='available_venues'),
        ))),

        url(r'^updates/(?P<scope>[-\w]+)/$', 'updates', name='updates'),
        url(r'^updates/(?P<scope>[-\w]+)/(?P<zipcode>[-\w]+)/$', 'updates', name='updates'),
    ))),


)
