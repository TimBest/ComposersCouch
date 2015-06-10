from django.conf.urls import patterns
from django.conf.urls import url


view_location = 'search.views'

urlpatterns = patterns(view_location,
    url(r'^$', 'search', name='search'),
)
