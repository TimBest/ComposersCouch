import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from . import forms
from .decorators import is_participant
from .models import Application, PrivateRequest, PublicRequest
from annoying.functions import get_object_or_None
from composersCouch.views import MultipleFormsView, MultipleModelFormsView
from customProfile.decorators import is_venue, is_musician
from threaded_messages.models import Message, Participant
from threaded_messages.views import MessageView
from threaded_messages.utils import reply_to_thread, create_thread


class PrivateRequestView(TemplateView):
    template_name='request/private_requests.html'

    def get_context_data(self, **kwargs):
        context = super(PrivateRequestView, self).get_context_data(**kwargs)
        context['participants'] = Participant.objects.filter(user=self.request.user)
        return context

private_requests = login_required(PrivateRequestView.as_view())

class PublicRequestView(TemplateView):
    template_name='request/public_requests.html'

    def get_context_data(self, **kwargs):
        context = super(PublicRequestView, self).get_context_data(**kwargs)
        context['requests'] = PublicRequest.objects.filter(requester=self.request.user)
        return context

public_requests = login_required(PublicRequestView.as_view())

class RequestView(MessageView):
    success_url='request_detail'
    template_name='request/view.html'

    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs)
        events = None
        context['calendar'] = calendar = self.request.user.calendar
        private_request = self.thread.request
        padding = datetime.timedelta(days=1)
        start = private_request.date.start - padding
        end = private_request.date.end + padding
        context['events'] = calendar.get_events_in_range(start=start, end=end)
        context['user_accept'] = private_request.has_accepted(self.request.user)
        context['host_accept'] = private_request.has_accepted(private_request.host)
        context['headliner_accept'] = private_request.has_accepted(private_request.headliner.profile.user)
        openers_accept = []
        for o in private_request.openers.all():
            openers_accept.append((o, private_request.has_accepted(o.profile.user)))
        context['openers_accept'] = openers_accept
        return context

view = RequestView.as_view()

class ApplicationView(MessageView):
    success_url='application_view'
    template_name='request/application_view.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationView, self).get_context_data(**kwargs)
        context['public_request'] = self.thread.application.public_request
        context['application'] = self.thread.application
        return context

application_view = ApplicationView.as_view()

""" Forms """
class RequestFormView(MultipleFormsView):
    form_classes = {
      'dateForm': forms.DateForm,
      'messageForm': forms.MessageForm,
      'requestForm': forms.PrivateRequestForm,
    }
    template_name = 'request/privaterequest_form.html'
    success_url = 'messages_inbox'

    def get_users(self):
        users = [self.request.user]
        username = self.kwargs.get('username', None)
        user = get_object_or_None(User, username=username)
        if user and self.request.user != user:
            users.append(user)
        return users

    def get_form_kwargs(self):
        kwargs = super(RequestFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial_data(self):
        request_data = {}
        date_data = {}
        for user in self.get_users():
            profile_type = user.profile.profile_type
            if profile_type == 'm':
                request_data['headliner'] = user.profile.musicianProfile
            elif profile_type == 'v' or profile_type == 'f' :
                request_data['host'] =  user
        return {
            'dateForm': date_data,
            'messageForm': None,
            'requestForm': request_data,
        }

    def get_success_url(self, private_request=None):
        # TODO: extend this guy to accept next urls
        thread = private_request.messages
        if thread:
            return redirect('request_detail', thread_id=thread.id)
        else:
            return redirect(success_url)

    def forms_valid(self, forms):
        private_request = forms['requestForm'].save(commit=False)
        private_request.date = forms['dateForm'].save()
        private_request.save()
        forms['requestForm'].save_m2m()
        private_request.messages = create_thread (
            participants=private_request.participants(),
            sender=self.request.user,
            subject="Show Request",
            body=forms['messageForm'].cleaned_data['body']
        )
        private_request.save()
        return self.get_success_url(private_request)

requestForm = login_required(RequestFormView.as_view())

class RequestEditFormView(MultipleModelFormsView):
    form_classes = {
      'dateForm': forms.DateForm,
      'requestForm': forms.EditPrivateRequestForm,
    }
    template_name = 'request/edit_request_form.html'

    def dispatch(self, *args, **kwargs):
        request_id = self.kwargs.get('request_id', None)
        self.private_request = get_object_or_None(PrivateRequest, id=request_id)
        return super(RequestEditFormView, self).dispatch(*args, **kwargs)

    def get_objects(self):
        return {
            'dateForm': self.private_request.date,
            'requestForm': self.private_request,
        }

    def forms_valid(self, forms):
        private_request = forms['requestForm'].save()
        private_request.date = forms['dateForm'].save()
        private_request.save()
        reply_to_thread(self.private_request.messages, self.request.user, "edited request")
        return self.get_success_url()

requestEditForm = is_participant(RequestEditFormView.as_view())

class PublicRequestFormView(MultipleFormsView):
    form_classes = {
      'dateForm': forms.DateForm,
      'requestForm': forms.PublicRequestForm,
    }
    template_name = 'request/publicrequest_form.html'
    success_url = 'home'

    def forms_valid(self, forms):
        date = forms['dateForm'].save()
        public_request = forms['requestForm'].save(commit=False)
        public_request.save(requester=self.request.user, date=date)
        return self.get_success_url()

public_request_form = is_musician(PublicRequestFormView.as_view())

class PublicBandRequestFormView(PublicRequestFormView):
    form_classes = {
      'dateForm': forms.DateForm,
      'requestForm': forms.PublicRequestForm,
      'numApplicantsForm': forms.NumberOfApplicantsForm,
    }
    template_name = 'request/publicrequest_form.html'
    success_url = 'home'

    def forms_valid(self, forms):
        date = forms['dateForm'].save()
        num_applicants = forms['numApplicantsForm'].save(commit=False)
        public_request = forms['requestForm'].save(commit=False)
        public_request.save(requester=self.request.user, date=date)
        num_applicants.save(public_request=public_request)
        return self.get_success_url()

public_band_request_form = login_required(PublicBandRequestFormView.as_view())


class ApplyFormView(FormView):
    form_class = forms.MessageForm
    success_url = 'messages_inbox'
    template_name = 'request/apply_form.html'

    def dispatch(self, *args, **kwargs):
        request_id = self.kwargs.get('request_id', None)
        self.public_request = get_object_or_None(PublicRequest, id=request_id)
        return super(ApplyFormView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApplyFormView, self).get_context_data(**kwargs)
        context['public_request'] = self.public_request
        return context

    def get_success_url(self):
        # TODO: extend this guy to accept next urls
        thread = self.app.thread
        if thread:
            return redirect('application_view', thread_id=thread.id)
        else:
            return redirect(success_url)

    def get_users(self):
        users = [self.public_request.requester,]
        if self.request.user != self.public_request.requester:
            users.append(self.request.user)
        return users


    def form_valid(self, form):
        thread = create_thread (
            participants=self.get_users(),
            sender=self.request.user,
            subject="Request Application",
            body=form.cleaned_data['body']
        )
        self.app = Application(public_request=self.public_request,thread=thread,applicant=self.request.user)
        self.app.save()
        return self.get_success_url()

appy_to_band = login_required(ApplyFormView.as_view())
appy_to_venue = is_musician(ApplyFormView.as_view())


@login_required
@require_POST
def approve(request, accept=True):
    # TODO: convert to ajax
    application = Application.objects.get(id=request.POST['application'])
    if application.public_request.requester == request.user:
        data = request.POST.copy()
        form = forms.ApproveForm(data=data)
        assert form.is_valid()
        form.save(application=application, approved=accept)
        return redirect('application_view', thread_id=application.thread.id)
    return PermissionDenied

def deny(request):
    return  approve(request, accept=False)

@login_required
@require_POST
def accept(request, accept=True):
    # TODO: convert to ajax
    private_request = PrivateRequest.objects.get(id=request.POST['private_request'])
    for user in private_request.participants():
        if user == request.user:
            data = request.POST.copy()
            form = forms.AcceptForm(data=data)
            assert form.is_valid()
            form.save(user=request.user,private_request=private_request, accepted=accept)
            return redirect('request_detail', thread_id=private_request.messages.id)
    return PermissionDenied

def decline(request):
    return  accept(request, accept=False)
