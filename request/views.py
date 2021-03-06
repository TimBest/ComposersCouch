import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms.formsets import formset_factory
from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from annoying.functions import get_object_or_None
from composersCouch.utils import get_page
from annoying.views import MultipleFormsView, MultipleModelFormsView
from customProfile.decorators import is_artist
from request import forms
from request.decorators import is_participant as is_request_participant
from request.models import Application, PrivateRequest, PublicRequest, RequestParticipant
from request.utils import send_request_email
from threads.decorators import is_participant
from threads.models import Message, Participant, Thread
from threads.views import MessageView
from threads.utils import reply_to_thread, create_thread


class PrivateRequestView(TemplateView):
    template_name='request/private_requests.html'

    def get_context_data(self, **kwargs):
        context = super(PrivateRequestView, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        context['inbox'] = True
        participants = Participant.objects.filter(
            user=self.request.user,
            deleted_at__isnull=True,
            thread__request__isnull=False,
        ).exclude(
            thread__creator=self.request.user,
        )
        context['participants'] = get_page(page_num, participants, 15)
        return context

inbox_private_requests = login_required(PrivateRequestView.as_view())

class SentPrivateRequestsView(TemplateView):
    template_name='request/private_requests.html'

    def get_context_data(self, **kwargs):
        context = super(SentPrivateRequestsView, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        context['sent'] = True
        participants = Participant.objects.filter(
            user=self.request.user,
            replied_at__isnull=False,
            deleted_at__isnull=True,
            thread__request__isnull=False,
        )
        context['participants'] = get_page(page_num, participants, 15)
        return context

sent_private_requests = login_required(SentPrivateRequestsView.as_view())

class PublicRequestView(TemplateView):
    template_name='request/public_requests.html'

    def get_context_data(self, **kwargs):
        context = super(PublicRequestView, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        requests = PublicRequest.objects.filter(requester=self.request.user)
        context['requests'] = get_page(page_num, requests, 15)
        context['is_requests'] = True
        return context

public_requests = login_required(PublicRequestView.as_view())

class PublicApplicationsView(TemplateView):
    template_name='request/public_applications.html'

    def get_context_data(self, **kwargs):
        context = super(PublicApplicationsView, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        applications = Application.objects.filter(applicant=self.request.user)
        context['applications'] = get_page(page_num, applications, 15)
        context['is_applications'] = True
        return context

public_applications = login_required(PublicApplicationsView.as_view())

class RequestView(MessageView):
    success_url='request_detail'
    template_name='request/view.html'

    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs)
        context['calendar'] = calendar = self.request.user.calendar
        private_request = self.thread.request
        padding = datetime.timedelta(days=1)
        start = private_request.date.start - padding
        end = private_request.date.end + padding
        context['events'] = calendar.get_events_in_range(start=start, end=end)
        return context

view = is_participant(RequestView.as_view())

class ApplicationView(MessageView):
    success_url='application_view'
    template_name='request/application_view.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationView, self).get_context_data(**kwargs)
        context['publicRequest'] = self.thread.application.public_request
        context['application'] = self.thread.application
        return context

application_view = is_participant(ApplicationView.as_view())

""" Forms """
class RequestFormView(MultipleFormsView):
    form_classes = {
      'dateForm'      : forms.DateForm,
      'messageForm'   : forms.MessageForm,
      'venueForm'      : forms.ParticipantForm,
    }
    model = Participant
    form_class = forms.ArtistParticipantForm
    template_name = 'request/forms/private_request.html'
    success_url = 'sent_private_requests'
    artist = {}

    def get_form_kwargs(self):
        kwargs = super(RequestFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_forms(self):
        requestForms = super(RequestFormView, self).get_forms()
        formset = formset_factory(self.form_class,
            formset=forms.ParticipantFormSet, max_num=3, min_num=3)
        if self.request.method == 'POST':
            requestForms['ArtistFormset'] = formset(**self.get_form_kwargs())
        else:
            requestForms['ArtistFormset'] = formset(initial=[self.artist],
                                                    **self.get_form_kwargs())
        return requestForms

    def get_initial_data(self):
        venue_data = {}
        for user in self.get_users():
            profile_type = user.profile.profile_type
            if profile_type == 'm':
                self.artist = {'user' : user}
            else:
                venue_data = {'user' : user}
        return {'dateForm':None, 'messageForm':None, 'venueForm':venue_data,}

    def get_success_url(self, thread=None):
        # TODO: extend this guy to accept next urls
        if thread:
            return redirect('request_detail', thread_id=thread.id)
        else:
            return redirect(self.success_url)

    def get_users(self):
        users = [self.request.user]
        username = self.kwargs.get('username', None)
        user = get_object_or_None(User, username=username)
        if user and self.request.user != user:
            users.append(user)
        return users

    def forms_valid(self, forms):
        sender = self.request.user
        message = Message.objects.create(
                    body=forms['messageForm'].cleaned_data['body'],
                    sender=sender,
                    parent_msg=None,
        )
        thread = Thread.objects.create(
            subject="Show Request",
            latest_msg=message,
            creator=sender,
        )
        thread.all_msgs.add(message)
        thread.save()
        for form in forms['ArtistFormset']:
            if form.cleaned_data.get('user'):
                form.save(thread=thread, sender=sender)
        private_request = PrivateRequest.objects.create(
            date=forms['dateForm'].save(),
            thread=thread,
        )
        private_request.save()
        forms['venueForm'].save(thread=thread, sender=sender, role='v')
        # check if user is in thread. if not add them
        participant = get_object_or_None(Participant ,thread=thread, user=sender)
        if not participant:
            participant = Participant(user=sender, thread=thread,
                                      read_at=now(), replied_at=now())
            participant.save()
            request_paticipant = RequestParticipant(participant=participant, role='o', accepted=True)
            request_paticipant.save()
        send_request_email(request=private_request)
        return self.get_success_url(thread)

requestForm = login_required(RequestFormView.as_view())

class RequestEditFormView(MultipleModelFormsView):
    form_classes = {
      'dateForm': forms.DateForm,
    }
    template_name = 'request/forms/edit_private_request.html'
    success_url = 'sent_private_requests'

    def dispatch(self, *args, **kwargs):
        request_id = self.kwargs.get('request_id', None)
        self.private_request = get_object_or_None(PrivateRequest, id=request_id)
        return super(RequestEditFormView, self).dispatch(*args, **kwargs)

    def get_objects(self):
        return {
            'dateForm': self.private_request.date,
        }

    def get_success_url(self, thread=None):
        # TODO: extend this guy to accept next urls
        if thread:
            return redirect('request_detail', thread_id=thread.id)
        else:
            return redirect(self.success_url)

    def forms_valid(self, forms):
        self.private_request.date = forms['dateForm'].save()
        self.private_request.save()
        reply_to_thread(self.private_request.thread, self.request.user, "edited request")
        return self.get_success_url(thread=self.private_request.thread)

requestEditForm = is_request_participant(RequestEditFormView.as_view())

class PublicRequestFormView(MultipleFormsView):
    form_classes = {
      'dateForm': forms.DateForm,
      'requestForm': forms.PublicRequestForm,
    }
    template_name = 'request/forms/public_request.html'
    success_url = 'public_requests'

    def forms_valid(self, forms):
        date = forms['dateForm'].save()
        public_request = forms['requestForm'].save(commit=False)
        public_request.save(requester=self.request.user, date=date)
        return self.get_success_url()

public_request_form = is_artist(PublicRequestFormView.as_view())

class PublicBandRequestFormView(PublicRequestFormView):
    form_classes = {
      'dateForm': forms.DateForm,
      'requestForm': forms.PublicRequestForm,
      'numApplicantsForm': forms.NumberOfApplicantsForm,
    }
    template_name = 'request/forms/public_request.html'
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
    success_url = 'public_requests'
    template_name = 'request/forms/apply.html'

    def dispatch(self, *args, **kwargs):
        request_id = self.kwargs.get('request_id', None)
        self.public_request = get_object_or_None(PublicRequest, id=request_id)
        return super(ApplyFormView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApplyFormView, self).get_context_data(**kwargs)
        context['publicRequest'] = self.public_request
        return context

    def get_success_url(self):
        # TODO: extend this guy to accept next urls
        thread = self.app.thread
        if thread:
            return redirect('application_view', thread_id=thread.id)
        else:
            return redirect(self.success_url)

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
appy_to_venue = is_artist(ApplyFormView.as_view())


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
    raise PermissionDenied

def deny(request):
    return  approve(request, accept=False)

@login_required
@require_POST
def accept(request, accept=True):
    # TODO: convert to ajax
    private_request = PrivateRequest.objects.get(
                        id=request.POST['private_request'])
    participant = get_object_or_None(Participant,thread=private_request.thread,
                                     user=request.user)
    if participant:
        for request_participant in participant.request_participant.all():
            request_participant.accepted = accept
            request_participant.save()
        return redirect('request_detail', thread_id=private_request.thread.id)
    raise PermissionDenied

def decline(request):
    return  accept(request, accept=False)
