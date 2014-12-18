from django.conf.urls import include, patterns, url


view_location = 'schedule.views'
urlpatterns = patterns(view_location,
    url(r'^calendar/', include(patterns(view_location,
        url(r'^year/(?P<calendar_slug>[-\w]+)/$', 'year', name="year_calendar"),
        url(r'^month/(?P<calendar_slug>[-\w]+)/$', 'month', name="month_calendar"),
        url(r'^week/(?P<calendar_slug>[-\w]+)/$', 'week', name="week_calendar"),
        url(r'^day/(?P<calendar_slug>[-\w]+)/$', 'day', name="day_calendar"),
    ))),

    url(r'^show/', include(patterns(view_location,
        url(r'^create/(?P<calendar_slug>[-\w]+)/$', 'create_event', name='calendar_create_event'),
        url(r'^edit/(?P<calendar_slug>[-\w]+)/(?P<show_id>\d+)/$', 'edit_event', name='edit_event'),
        url(r'^requestToEvent/(?P<calendar_slug>[-\w]+)/(?P<request_id>\d+)/$', 'request_to_event', name='calendar_request_to_event'),
        url(r'^view/(?P<calendar_slug>[-\w]+)/(?P<show_id>\d+)/$', 'show', name="show"),
        url(r'^view-message/(?P<thread_id>\d+)/$', 'show_message', name="show_message"),
        url(r'^confirm/$', 'confirm', name='show_confirm'),
        url(r'^deny/$', 'deny', name='show_deny'),
    ))),
)
