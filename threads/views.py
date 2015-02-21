# -*- coding:utf-8 -*-
import logging, datetime
from django.contrib.auth import login, BACKEND_SESSION_KEY
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator

from .models import *
from .decorators import is_participant
from .forms import ComposeForm, ReplyForm
from .utils import fill_count_cache, now


class threadMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(threadMixin, self).dispatch(*args, **kwargs)

class InboxView(threadMixin, TemplateView):
    """
    Displays a list of received messages for the current user.
    """
    template_name = 'threads/inbox.html'

    def get_context_data(self, **kwargs):
        return {
            'message_list': Participant.objects.inbox_for(self.request.user),
        }

inbox = InboxView.as_view()

class SentView(threadMixin, TemplateView):
    """
    Displays a list of sent messages for the current user.
    """
    template_name = 'threads/sent.html'

    def get_context_data(self, **kwargs):
        return {
            'message_list': Participant.objects.outbox_for(self.request.user),
        }

sent = SentView.as_view()

class TrashView(threadMixin, TemplateView):
    """
    Displays a list of deleted messages for the current user.
    """
    template_name = 'threads/trash.html'

    def get_context_data(self, **kwargs):
        return {
            'message_list': Participant.objects.trash_for(self.request.user),
        }

trash = TrashView.as_view()

class ComposeView(threadMixin, FormView):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
    """
    form_class=ComposeForm
    success_url='threads:sent'
    template_name='threads/compose.html'

    def form_valid(self, form):
        form.save(sender=self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        recipients = None
        recipient = self.kwargs.get('recipient')
        if recipient is not None:
            recipients = [u for u in User.objects.filter(username__in=[r.strip() for r in recipient.split('+')])]
        return {
            'recipients' : recipients
        }

    def get_success_url(self, **kwargs):
        if self.request.GET.has_key('next'):
            return self.request.GET['next']
        else:
            return reverse(self.success_url, **kwargs)

compose = ComposeView.as_view()

class MessageView(threadMixin, FormView):
    form_class=ReplyForm
    success_url='threads:detail'
    template_name='threads/view.html'

    @method_decorator(is_participant)
    def dispatch(self, *args, **kwargs):
        thread_id = kwargs.get('thread_id')
        self.thread = get_object_or_404(Thread, id=thread_id)
        return super(MessageView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save(sender=self.request.user, thread=self.thread)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context['thread'] = self.thread
        context['participant'] = participant = Participant.objects.filter(thread=self.thread, user=self.request.user)[0]
        message_list = []
        # in this view we want the last message last
        for message in self.thread.all_msgs.all().order_by("sent_at"):
            unread = True
            if participant.read_at and message.sent_at <= participant.read_at:
                unread = False
            message_list.append((message, unread,))
        context['message_list'] = message_list
        participant.read_thread()
        return context

    def get_success_url(self, **kwargs):
        return reverse(success_url, args=(self.thread.id,))

view = MessageView.as_view()

@login_required
def batch_update(request, success_url=None):
    """
    Gets an array of message ids which can be either deleted or marked as
    read/unread
    """
    if request.method == "POST":
        ids = request.POST.getlist("batchupdateids")
        if ids:
            threads = Thread.objects.filter(pk__in=ids)
            for thread in threads:
                participant = thread.participants.filter(user=request.user)
                if participant:
                    participant = participant[0]
                    if request.POST.get("action") == "read":
                        participant.read_at = now()
                    elif request.POST.get("action") == "delete":
                        participant.deleted_at = now()
                    elif request.POST.get("action") == "restore":
                        participant.deleted_at = None
                    elif request.POST.get("action") == "unread":
                        participant.read_at = None
                    participant.save()
            # update the inbox count
            fill_count_cache(request.user)
    else:
        # this should only happen when hacked or developer uses wrong, therefore
        # return simple message
        return HttpResponse("Only Post allowed", code=400)

    if success_url:
        return HttpResponseRedirect(success_url)
    else:
        # either go to last page, or to inbox as fallback
        referer = request.META.get('HTTP_REFERER', None)
        if referer:
            return HttpResponseRedirect(referer)
        else:
            return HttpResponseRedirect(reverse("threads:inbox"))

@is_participant
def message_ajax_reply(request, thread_id, success_url='threads:inbox'):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.POST:
        form = ReplyForm(data=request.POST)
        if form.is_valid():
            try:
                (thread, new_message) = form.save(sender=request.user, thread=thread)
            except Exception, e:
                logging.exception(e)
                return HttpResponse(status=500, content="Message could not be sent")

            return render_to_response('threads/_message.html', {'message':new_message,'user':request.user})
        else:
            print form.errors
            return HttpResponse(status=400, content="Invalid Form")
