from django.conf.urls import include, patterns, url


view_location = 'customProfile.views'
urlpatterns = patterns(view_location,
    # News Tab
    url(r'^$',
        'profileRedirect',
        {'redirect_url': 'venue:news'},
        name='home'),
    url(r'^news/$',
        'venue_news',
        name='news'),
    # About Tab
    url(r'^about/', include(patterns(view_location,
        url(r'^links/edit/$',
            'venue_social_links',
            name='socialLinksForm'),
    ))),
    # Shows Tab
    url(r'^shows/', include(patterns(view_location,
        url(r'^$',
            'venue_shows',
            name='shows'),
        url(r'^(?P<year>\d{4})/$',
            'venue_shows',
            name='shows'),
    ))),
    # Photos Tab
    url(r'^photos/', include(patterns(view_location,
        url(r'^$',
            'venue_photos',
            name='photos'),
        url(r'^links/edit/$',
            'venue_photo_links',
            name='photoLinksForm'),
    ))),
)

view_location = 'customProfile.venue.views'
urlpatterns += patterns(view_location,

    # About Tab
    url(r'^about/', include(patterns(view_location,
        url(r'^$',
            'venue_about',
            name='about'),
        # Forms
        url(r'^biography/edit/$',
            'biography',
            name='biographyForm'),
        url(r'^contact/edit/$',
            'contact_info',
            name='contactForm'),
        url(r'^equipment/edit/(?P<category>[\.\w-]+)/$',
            'equipment',
            name='equipmentForm'),
        url(r'^hours/edit/$',
            'hours',
            name='hoursForm'),
        url(r'^policies/edit/$',
            'policies',
            name='policiesForm'),
        url(r'^seating/edit/$',
            'seating',
            name='seatingForm'),
        url(r'^staff/edit/$',
            'staff',
            name='staffForm'),
        url(r'^staff/edit/(?P<staffID>[\.\w-]+)/$',
            'staff',
            name='staffForm'),
    ))),

)
