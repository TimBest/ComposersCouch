from django.conf.urls import include, patterns, url
from django.views.generic.base import RedirectView


urlpatterns = patterns('messages.views',
    url(r'^$', RedirectView.as_view(url='inbox/')),
    url(r'^inbox/$', 'inbox', name='messages_inbox'),
    url(r'^sent/$', 'sent', name='messages_sent'),
    url(r'^compose/$', 'compose', name='messages_compose'),
    url(r'^compose/(?P<recipient>[\+\w]+)/$', 'compose', name='messages_compose'),
    url(r'^view/(?P<thread_id>[\d]+)/$', 'view', name='messages_detail'),
    url(r'^delete/(?P<thread_id>[\d]+)/$', 'delete', name='messages_delete'),
    url(r'^restore/(?P<thread_id>[\d]+)/$', 'restore', name='messages_restore'),
    url(r'^batch-update/$', 'batch_update', name='messages_batch_update'),
    url(r'^trash/$', 'trash', name='messages_trash'),

    url(r'^message-reply/(?P<thread_id>[\d]+)/$', 'message_ajax_reply', name="message_reply"),

)
