from django.conf.urls import include, patterns, url


view_location = 'customProfile.views'
urlpatterns = patterns(view_location,
    # Views
    url(r'^(?P<username>[-\w]+)/', include(patterns(view_location,
        url(r'^$', 'profileRedirect', {'redirect_url': 'venue:about'}, name='home'),
        url(r'^news/$', 'venue_news', name='news'),
        url(r'^shows/$','venue_shows', name='shows'),
        url(r'^shows/(?P<year>\d{4})/$','venue_shows',name='shows'),
        url(r'^photos/$', 'venue_photos', name='photos'),
    ))),

    # Forms
    url(r'^about/links/edit/$', 'venue_social_links', name='socialLinksForm'),
    url(r'^photos/links/edit/$', 'venue_photo_links', name='photoLinksForm'),
)

view_location = 'venue.views'
urlpatterns += patterns(view_location,
    # Views
    url(r'^(?P<username>[-\w]+)/', include(patterns(view_location,
        url(r'^about/$', 'venue_about', name='about'),
    ))),

    #Forms
    url(r'^about/', include(patterns(view_location,
        url(r'^biography/edit/$', 'biography', name='biographyForm'),
        url(r'^contact/edit/$', 'contact_info', name='contactForm'),
        url(r'^equipment/edit/(?P<category>[\.\w-]+)/$', 'equipment', name='equipmentForm'),
        url(r'^hours/edit/$', 'hours', name='hoursForm'),
        url(r'^policies/edit/$','policies',name='policiesForm'),
        url(r'^seating/edit/$', 'seating', name='seatingForm'),
        url(r'^staff/edit/$', 'staff', name='staffForm'),
        url(r'^staff/edit/(?P<staffID>[\.\w-]+)/$', 'staff', name='staffForm'),
    ))),
)
