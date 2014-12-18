from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('composersCouch.views',
    #url(r'^$',
    #    'home',
    #    name='home'),
    url(r'^team/$',
        'load_template',
        {'template_name': 'footer/team.html'},
        name='team'),
    url(r'^credit/$',
        'load_template',
        {'template_name': 'footer/credit.html'},
        name='credit'),
    url(r'^colorScheme/$',
        'load_template',
        {'template_name': 'footer/colors.html'},
        name='colors'),
)
