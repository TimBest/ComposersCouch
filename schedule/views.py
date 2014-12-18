import datetime
from urllib import quote
from urlparse import urlparse

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils import decorators
from django.views.decorators.http import require_POST
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView

from annoying.functions import get_object_or_None
from composersCouch.views import MultipleModelFormsView
from messages.views import MessageView
from messages.utils import create_thread
from photos.models import Image
from photos.forms import PosterForm
from photos.views import ImageFormMixin
from request.models import PrivateRequest
from schedule.forms import DateForm, EventForm, ShowInfoForm
from schedule.models import Calendar, Event, Show
from schedule.periods import weekday_names, Year, Month, Week, Day
from schedule.utils import view_show, edit_show, coerce_date_dict

edit_show_m = decorators.method_decorator(edit_show)
login_required_m = decorators.method_decorator(login_required)


""" Calendar Views """
class CalendarView(TemplateView):
    period = Month
    template_name = 'schedule/calendar_month.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        calendar_slug = kwargs.get('calendar_slug', None)
        self.calendar = get_object_or_None(Calendar, slug=calendar_slug)
        if self.calendar != self.request.user.calendar:
            path = self.request.path_info
            url = resolve(urlparse(path)[2])
            return redirect(url.url_name, calendar_slug=self.request.user.calendar.slug)
        return super(CalendarView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CalendarView, self).get_context_data(*args, **kwargs)
        context['calendar'] = self.calendar
        context['date'] = coerce_date_dict(self.request.GET)
        event_list = self.calendar.events.filter(approved=True)
        context['periods'] = dict([(self.period.__name__.lower(), self.period(event_list, context['date']))])
        context['weekday_names'] = weekday_names
        context['here'] = quote(self.request.get_full_path()),
        return context
month = CalendarView.as_view()

class YearView(CalendarView):
    period = Year
    template_name = 'schedule/calendar_year.html'
year = YearView.as_view()

class WeekView(CalendarView):
    period = Week
    template_name = 'schedule/calendar_week.html'
week = WeekView.as_view()

class DayView(CalendarView):
    period = Day
    template_name = 'schedule/calendar_day.html'
day = DayView.as_view()

""" Show Views """
class ShowView(TemplateView):
    template_name="schedule/show.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ShowView, self).get_context_data(*args, **kwargs)
        show_id = kwargs.get('show_id', None)
        calendar_slug = kwargs.get('calendar_slug', None)
        context['show'] = show = get_object_or_None(Show, id=show_id)
        context['calendar'] = calendar = get_object_or_None(Calendar, slug=calendar_slug)
        event = get_object_or_None(Event, show=show, calendar=calendar)
        context['user_accept'] = event.approved
        return context

show = view_show(ShowView.as_view())

class ShowMessageView(MessageView):
    success_url='show_message'
    template_name='schedule/message.html'

    def get_context_data(self, **kwargs):
        context = super(ShowMessageView, self).get_context_data(**kwargs)
        context['calendar'] = self.request.user.calendar
        return context

show_message = ShowMessageView.as_view()



""" Forms """
class EventFormView(ImageFormMixin, MultipleModelFormsView):
    form_classes = {
      'date_form' : DateForm,
      'event_form': EventForm,
      'show_info_form' : ShowInfoForm,
      'poster_form': PosterForm,
    }
    template_name='schedule/create_event.html'
    success_url = 'month_calendar'
    images_on_page = 6

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(EventFormView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EventFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_objects(self, queryset=None):
        return {'poster_form':None,'date_form':None,'event_form':None,'show_info_form':None,}

    def get_initial_data(self):
        show_data = {}
        date_data = {"start": coerce_date_dict(self.request.GET),}
        if self.request.user.profile.profile_type == "m":
            show_data['headliner'] = self.request.user.profile.musicianProfile
        else:
            show_data['host'] = self.request.user
        return {'poster_form':{},'date_form':date_data,'event_form':{},'show_info_form':show_data,}

    def forms_valid(self, forms):
        poster_form = forms['poster_form']
        date  = forms['date_form'].save()
        info  = forms['show_info_form'].save(commit=False)

        if self.request.FILES.get('image'):
            info.poster = Image.objects.create(
                image=self.request.FILES.get('image'),
                title = "Poster",
                user = self.request.user
            )
        elif self.request.POST.get('poster'):
            imageId = self.request.POST.get('poster')
            info.poster = get_object_or_None(Image, id=imageId)

        if not info.location:
            info.location = info.host.profile.contact_info.location
        info.save()
        forms['show_info_form'].save_m2m()
        participants = info.participants()
        thread = create_thread (
            participants=participants,
            sender=self.request.user,
            subject="Event Thread",
            body="View the shows details: <a href="+"url"+">here</a>",
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
        return self.get_success_url(calendar_slug=self.request.user.calendar.slug)

create_event = EventFormView.as_view()

class EditEventFormView(EventFormView):
    success_url = 'month_calendar'

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
            'event_form' : Event(show=self.show, calendar=self.request.user.calendar),
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
            info.poster = Image.objects.create(
                image=self.request.FILES.get('image'),
                title = "Poster",
                user = self.request.user
            )
        elif self.request.POST.get('poster'):
            imageId = self.request.POST.get('poster')
            info.poster = get_object_or_None(Image, id=imageId)

        if not info.location:
            info.location = info.host.profile.contact_info.location
        info.save()
        forms['show_info_form'].save_m2m()
        participants = info.participants()

        # create or edit event for each particpent in show
        for user in participants:
            if self.request.user != user:
                event = get_object_or_None(Event, show=self.show, calendar=user.calendar)
                if not event:
                    event = Event(show=self.show, calendar=user.calendar)
                    event.save()
        return self.get_success_url(calendar_slug=self.request.user.calendar.slug)

edit_event = EditEventFormView.as_view()

class RequestToEventFormView(EventFormView):

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
        show_data = {
            "headliner": self.private_request.headliner,
            "openers"  : self.private_request.openers.all(),
            "host"     : self.private_request.host,
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
    return redirect('messages_detail', thread_id=show.thread.id)

def deny(request):
    return  confirm(request, approved=False)