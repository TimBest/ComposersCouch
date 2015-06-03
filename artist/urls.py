from django.conf.urls import include, patterns, url


view_location = 'customProfile.views'
urlpatterns = patterns(view_location,
    # Views
    url(r'^(?P<username>[-\w]+)/', include(patterns(view_location,
        url(r'^$', 'profileRedirect', {'redirect_url': 'artist:about'}, name='home'),
        url(r'^news/$', 'artist_news', name='news'),
        url(r'^shows/$','shows', name='shows'),
        url(r'^shows/(?P<year>\d{4})/$','shows',name='shows'),
        url(r'^photos/$', 'artist_photos', name='photos'),
    ))),

)

view_location = 'social_links.views'
urlpatterns += patterns(view_location,
    # Forms
    url(r'^about/links/edit/$', 'artist_social_links', name='socialLinksForm'),
    url(r'^photos/links/edit/$', 'artist_photo_links', name='photoLinksForm'),
    url(r'^music/links/edit/$', 'music_links', name='musicLinksForm'),
    url(r'^videos/links/edit/$', 'artist_video_links', name='videoLinksForm'),
)

view_location = 'artist.views'
urlpatterns += patterns(view_location,
    # Views
    url(r'^(?P<username>[-\w]+)/', include(patterns(view_location,
        url(r'^about/$', 'about', name='about'),
        url(r'^music/$', 'music', name='music'),
        url(r'^videos/$', 'videos', name='videos'),
    ))),

    #Forms
    url(r'^about/', include(patterns(view_location,
        url(r'^biography/edit/$', 'biography', name='biographyForm'),
        url(r'^contact/edit/$', 'contact_info', name='userContactForm'),
        url(r'^member/add/$', 'members', name='memberForm'),
        url(r'^member/edit/(?P<member_id>[\.\w-]+)$', 'members', name='memberForm'),
        url(r'^(?P<contact_type>[\.\w-]+)/edit/$', 'contacts', name='contactForm'),
    ))),
    url(r'^music/', include(patterns(view_location,
        url(r'^album/add/$', 'AddEditAlbum', name='albumForm'),
        url(r'^album/(?P<album_id>[\.\w-]+)/edit/$', 'AddEditAlbum', name='editAlbumForm'),
        url(r'^album/(?P<album_id>[\.\w-]+)/tracks/add/$', 'AddEditTracks', name='tracksForm'),
        #url(r'^interview/add/$', 'interview_form', name='interview_form'),
        #url(r'^interview/add/(?P<trackID>[\.\w-]+)$', 'interview_form', name='interview_form'),
    ))),
    url(r'^videos/', include(patterns(view_location,
        url(r'^album/add/$', 'AddEditAlbum', {'success_url': 'artist:video_tracks_form'}, name='video_album_form'),
        url(r'^album/(?P<album_id>[\.\w-]+)/edit/$', 'AddEditAlbum', {'success_url': 'artist:video_tracks_form'}, name='video_edit_album'),
        url(r'^album/(?P<album_id>[\.\w-]+)/tracks/add/$', 'add_video_to_album', name='video_tracks_form'),
        #url(r'^interview-video/add/$', 'interview_video_form', name='interview_video_form'),
        #url(r'^interview-video/add/(?P<trackID>[\.\w-]+)$', 'interview_video_form', name='interview_video_form'),
    ))),
)
