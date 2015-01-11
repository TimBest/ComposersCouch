from django.conf.urls import patterns, url


urlpatterns = patterns('photos.views',
     url(r'^upload/$', 'create_image', name='upload'),
     url(r'^(?P<pk>\d+)/$', 'veiw_image', name='image'),
     url(r'^delete/(?P<pk>\d+)/$', 'delete_image', name='delete-image'),
     url(r'^update/(?P<pk>\d+)/$', 'update_image', name='update-image'),

)
