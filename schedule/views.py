from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils import decorators, timezone
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from datetime import datetime

from annoying.functions import get_object_or_None
from annoying.views import MultipleModelFormsView
from threads.models import Participant
from threads.views import MessageView
from threads.utils import create_thread
from photos.models import Image
from photos.forms import PosterForm
from photos.views import ImageFormMixin
from request.decorators import is_participant
from request.models import PrivateRequest
from schedule.forms import DateForm, EventForm, ShowInfoForm
from schedule.models import Calendar, Event, Show
from schedule.periods import Year, Month, Week, Day
from schedule.utils import coerce_date_dict, export
from schedule.decorators import view_show, edit_show


view_show_m = decorators.method_decorator(view_show)
edit_show_m = decorators.method_decorator(edit_show)
login_required_m = decorators.method_decorator(login_required)
is_participant_m = decorators.method_decorator(is_participant)

PERIODS = {
    'day'   : (Day,  'schedule/calendar_day.html'),
    'week'  : (Week, 'schedule/calendar_week.html'),
    'month' : (Month,'schedule/calendar_month.html'),
    'year'  : (Year, 'schedule/calendar_year.html'),
}

FILTER = ['shows', 'requests']


""" Calendar Views """
class CalendarView(TemplateView):
    period = Month
    template_name = 'schedule/calendar_month.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        period_name = kwargs.get('period', None)
        self.period, self.template_name = PERIODS.get(period_name, (self.period, self.template_name))
        return super(CalendarView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CalendarView, self).get_context_data(*args, **kwargs)
        context['calendar'] = self.request.user.calendar
        context['date'] = coerce_date_dict(self.request.GET)
        context['filter'] = filter = kwargs.get('filter')
        if filter == 'requests':
            event_list = Participant.objects.filter(user=self.request.user, thread__request__isnull=False)
        else:
            context['filter'] = filter = 'shows'
            event_list = self.request.user.calendar.events.filter(approved=True)
        tz = timezone.get_current_timezone()
        if tz:
            context['period'] = self.period(event_list, context['date'], tzinfo=tz)
        else:
            context['period'] = self.period(event_list, context['date'])

        context['period_name'] = self.period.__name__.lower()
        return context

calendar = CalendarView.as_view()

""" Show Views """
class ShowView(TemplateView):
    template_name="schedule/show.html"

    @view_show_m
    def dispatch(self, *args, **kwargs):
        show_id = self.kwargs.get('show_id', None)
        self.show = get_object_or_None(Show, id=show_id)
        try:
            event = get_object_or_None(Event, show=self.show, calendar=self.request.user.calendar)
        except:
            event = None
        if event:
            return redirect('show_message', thread_id=self.show.thread.id)
        else:
            return super(ShowView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ShowView, self).get_context_data(*args, **kwargs)
        context['show'] = self.show
        return context

show = ShowView.as_view()

class ShowMessageView(MessageView):
    success_url='show_message'
    template_name='schedule/message.html'

    def get_context_data(self, **kwargs):
        context = super(ShowMessageView, self).get_context_data(**kwargs)
        context['calendar'] = self.request.user.calendar
        context['show'] = context['thread'].show
        return context

show_message = ShowMessageView.as_view()

def export_event(request, show_id):
    return export(shows=[get_object_or_None(Show, id=show_id),])

""" Forms """
class EventFormView(ImageFormMixin, MultipleModelFormsView):
    form_classes = {
      'date_form' : DateForm,
      'event_form': EventForm,
      'show_info_form' : ShowInfoForm,
      'poster_form': PosterForm,
    }
    template_name='schedule/forms/create_event.html'
    success_url = 'calendar'
    images_on_page = 6

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(EventFormView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EventFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        # if post add date start
        return kwargs

    def get_objects(self, queryset=None):
        return {'poster_form':None,'date_form':None,'event_form':None,'show_info_form':None,}

    def get_initial_data(self):
        show_data = {}
        date_data = {"start": coerce_date_dict(self.request.GET),}
        if self.request.user.profile.profile_type == "m":
            show_data['headliner_text'] = self.request.user.profile
            show_data['headliner'] = self.request.user.profile.artist_profile
        else:
            show_data['venue_text'] = self.request.user.profile
            show_data['venue'] = self.request.user
        return {'poster_form':{},'date_form':date_data,'event_form':{},'show_info_form':show_data,}

    def forms_valid(self, forms):
        poster_form = forms['poster_form']
        date  = forms['date_form'].save()
        info  = forms['show_info_form'].save(commit=False)

        if self.request.FILES.get('image'):
            info.poster, created = Image.objects.get_or_create(
                image=self.request.FILES.get('image'),
                title = "Poster",
                user = self.request.user
            )
        elif self.request.POST.get('poster'):
            imageId = self.request.POST.get('poster')
            info.poster = get_object_or_None(Image, id=imageId)

        if not info.location:
            if info.venue:
                info.location = info.venue.profile.contact_info.location
            else:
                info.location = self.request.user.profile.contact_info.location
        info.save()
        forms['show_info_form'].save_m2m()
        participants = info.participants()
        thread = create_thread (
            participants=participants,
            sender=self.request.user,
            subject="Event Thread",
            body=str(self.request.user.profile) + " added you in an event",
        )
        show = Show(info=info, date=date, thread=thread, approved=False)
        show.save()

        # create or edit event for each particpent in show
        for user in participants:
            if self.request.user != user:
                event = get_object_or_None(Event, show=show, calendar=user.calendar)
                if not event:
                    event = Event(show=show, calendar=user.calendar)
            else:
                event = forms['event_form'].save(commit=False)
                event.show = show
                event.calendar = user.calendar
                event.approved = True
            event.save()
        show.save()
        return self.get_success_url()

create_event = EventFormView.as_view()

class EditEventFormView(EventFormView):
    success_url = 'calendar'

    @edit_show_m
    def dispatch(self, *args, **kwargs):
        show_id = self.kwargs.get('show_id', None)
        self.show = get_object_or_None(Show, id=show_id)
        return super(EditEventFormView, self).dispatch(*args, **kwargs)

    def get_objects(self, queryset=None):
        info = getattr(self.show, 'info', None)
        return {
            'poster_form': getattr(info, 'poster', None),
            'date_form'  : self.show.date,
            'event_form' : get_object_or_None(Event, show=self.show, calendar=self.request.user.calendar),
            'show_info_form'  : info,
        }
    def get_initial_data(self):
        return {'poster_form':{},'date_form':{},'event_form':{},'show_info_form':{},}

    def forms_valid(self, forms):
        date  = forms['date_form'].save()
        self.show.date = date
        poster_form = forms['poster_form']
        info  = forms['show_info_form'].save(commit=False)

        if self.request.FILES.get('image'):
            info.poster, created = Image.objects.get_or_create(
                image=self.request.FILES.get('image'),
                title = "Poster",
                user = self.request.user
            )
        elif self.request.POST.get('poster'):
            imageId = self.request.POST.get('poster')
            info.poster = get_object_or_None(Image, id=imageId)

        if not info.location:
            info.location = info.venue.profile.contact_info.location
        info.save()
        forms['show_info_form'].save_m2m()
        participants = info.participants()

        # create or edit event for each particpent in show
        forms['event_form'].save()
        for user in participants:
            event = get_object_or_None(Event, show=self.show, calendar=user.calendar)
            if self.request.user != user and not event:
                event = Event(show=self.show, calendar=user.calendar)
                event.save()
        self.show.save()
        return self.get_success_url()

edit_event = EditEventFormView.as_view()

class RequestToEventFormView(EventFormView):

    @is_participant_m
    def dispatch(self, *args, **kwargs):
        request_id = self.kwargs.get('request_id', None)
        self.private_request = get_object_or_None(PrivateRequest, id=request_id)
        return super(RequestToEventFormView, self).dispatch(*args, **kwargs)

    def get_objects(self, queryset=None):
        return {
            'poster_form': None,
            'date_form'  : self.private_request.date,
            'event_form' : None,
            'show_info_form'  : None,
        }

    def get_initial_data(self):
        headliner = self.private_request.headliner()
        venue = self.private_request.venue()
        artists = self.private_request.openers()
        openers_text = ""
        openers = []
        for artist in artists:
            openers.append(artist.participant.user)
            openers_text = openers_text + str(artist.participant.user.profile) + ","
        show_data = {
            "headliner_text": headliner.participant.user.profile if headliner else None,
            "headliner": headliner.participant.user if headliner else None,
            "openers"  : openers,
            "openers_text"  : openers_text,
            "venue_text": venue.participant.user.profile if venue else None,
            "venue": venue.participant.user if venue else None,
        }
        return {'poster_form':{},'date_form':{},'event_form':{},'show_info_form':show_data,}

request_to_event = RequestToEventFormView.as_view()

@login_required
@require_POST
def confirm(request, approved=True):
    # TODO: convert to ajax
    show = Show.objects.get(id=request.POST['show'])
    event = get_object_or_None(Event, show=show, calendar=request.user.calendar)
    if event:
        event.approved=approved
        event.save()
    else:
        raise PermissionDenied
    return redirect('show_message', thread_id=show.thread.id)

def deny(request):
    return confirm(request, approved=False)
