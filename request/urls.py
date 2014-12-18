from django.conf.urls import include, patterns, url


urlpatterns = patterns('request.views',
    url(r'^view/(?P<thread_id>[\d]+)/$', 'view', name='request_detail'),
    url(r'^application/view/(?P<thread_id>[\d]+)/$', 'application_view', name='application_view'),
    # Forms
    url(r'^$', 'requestForm', name='request_write'),
    url(r'^public/$', 'public_request_form', name='public_request'),
    url(r'^public/band/$', 'public_band_request_form', name='public_band_request'),
    url(r'^accept/$', 'accept', name='request_accept'),
    url(r'^decline/$', 'decline', name='request_decline'),
    url(r'^approve/$', 'approve', name='approve_public_request'),
    url(r'^deny/$', 'deny', name='deny_public_request'),
    url(r'^apply-to-band/(?P<request_id>[-\w]+)/$', 'appy_to_band', name='request_appy_to_band'),
    url(r'^apply-to-venue/(?P<request_id>[-\w]+)/$', 'appy_to_venue', name='request_appy_to_venue'),
    url(r'^create/(?P<username>[-\w]+)/$', 'requestForm', name='request_write'),
    url(r'^edit/(?P<request_id>[-\w]+)/$', 'requestEditForm', name='request_edit'),
)
