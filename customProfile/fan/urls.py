from django.conf.urls import include, patterns, url


view_location = 'customProfile.views'
urlpatterns = patterns(view_location,
    # News Tab
    url(r'^$',
        'profileRedirect',
        {'redirect_url': 'fan:news'},
        name='home'),
    url(r'^news/$',
        'fan_news',
        name='news'),
    # Photos
    url(r'^photos/', include(patterns(view_location,
        url(r'^$',
            'fan_photos',
            name='photos'),
    ))),
)
"""
view_location = 'customProfile.fan.views'
urlpatterns += patterns(view_location,

)
"""
