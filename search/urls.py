from django.conf.urls import include, patterns, url


view_location = 'search.views'

urlpatterns = patterns(view_location,
    url(r'^$', 'search', name='search'),
)
