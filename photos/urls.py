try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from views import (ImageListView, UpdateImage, CreateImage, DeleteImage,
                   ImageView)


urlpatterns = patterns('photos.views',
     url(r'^tag/(?P<tag>[^/]+)/$', ImageListView.as_view(), name='tag'),

     url(r'^user/(?P<username>\w+)/$', ImageListView.as_view(), name='user-images'),

     url(r'^upload/$', CreateImage.as_view(), name='upload'),

     url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
     url(r'^album/(?P<album_id>\d+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='image-album'),
     url(r'^tag/(?P<tag>[^/]+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='image-tag'),
     url(r'^image/(?P<pk>\d+)/delete/$', DeleteImage.as_view(), name='delete-image'),
     url(r'^image/(?P<pk>\d+)/update/$', UpdateImage.as_view(), name='update-image'),
)



