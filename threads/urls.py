from django.conf.urls import include, patterns, url
from django.views.generic.base import RedirectView


urlpatterns = patterns('threads.views',
    url(r'^$', 'inbox', name='inbox'),
    url(r'^sent/$', 'sent', name='sent'),
    url(r'^trash/$', 'trash', name='trash'),
    url(r'^compose/$', 'compose', name='compose'),
    url(r'^compose/(?P<recipient>[\+\w]+)/$', 'compose', name='compose'),
    url(r'^view/(?P<thread_id>[\d]+)/$', 'view', name='detail'),
    url(r'^batch-update/$', 'batch_update', name='batch_update'),
    url(r'^message-reply/(?P<thread_id>[\d]+)/$', 'message_ajax_reply', name="reply"),

)
