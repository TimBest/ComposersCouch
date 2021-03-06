import pytz, datetime
import calendar as standardlib_calendar

from django.conf import settings
from django.template.defaultfilters import date as date_filter
from django.utils.translation import ugettext
from django.utils import timezone


class Period(object):
    """
    This class represents a period of time. It can return a set of shows
    based on its time period (start and end).
    """
    def __init__(self, events, start, end,  tzinfo=pytz.utc):
        self.utc_start = self._normalize_timezone_to_utc(start, tzinfo)
        self.utc_end = self._normalize_timezone_to_utc(end, tzinfo)
        self.events = events
        self.tzinfo = self._get_tzinfo(tzinfo)


    def _normalize_timezone_to_utc(self, point_in_time, tzinfo):
        if point_in_time.tzinfo is not None:
            return point_in_time.astimezone(pytz.utc)
        if tzinfo is not None:
            return tzinfo.localize(point_in_time).astimezone(pytz.utc)
        if settings.USE_TZ:
            return pytz.utc.localize(point_in_time)
        else:
            if timezone.is_aware(point_in_time):
                return timezone.make_naive(point_in_time, pytz.utc)
            else:
                return point_in_time

    def __eq__(self, period):
        return self.utc_start == period.utc_start and self.utc_end == period.utc_end and self.events == period.events

    def __ne__(self, period):
        return self.utc_start != period.utc_start or self.utc_end != period.utc_end or self.events != period.events

    def _get_tzinfo(self, tzinfo):
        return tzinfo if settings.USE_TZ else None

    def classify_event(self, event):
        if hasattr(event, 'show'):
            if event.show.date.start > self.end or event.show.date.end < self.start:
                return None
        else:
            if event.thread.request.date.start > self.end or event.thread.request.date.end < self.start:
                return None
        return event

    def get_event_partials(self):
        event_dicts = []
        for event in self.events:
            event = self.classify_event(event)
            if event:
                event_dicts.append(event)
        return event_dicts

    def get_time_slot(self, start, end):
        if start >= self.start and end <= self.end:
            return Period(self.events, start, end)
        return None

    def create_sub_period(self, cls, start=None, tzinfo=None):
        if tzinfo is None:
            tzinfo = self.tzinfo
        start = start or self.start
        return cls(self.events, start, tzinfo)

    def get_periods(self, cls, tzinfo=None):
        if tzinfo is None:
            tzinfo = self.tzinfo
        period = self.create_sub_period(cls)
        while period.start < self.end:
            yield self.create_sub_period(cls, period.start, tzinfo)
            period = period.next()

    @property
    def start(self):
        if self.tzinfo is not None:
            return self.utc_start.astimezone(self.tzinfo)
        return self.utc_start.replace(tzinfo=None)

    @property
    def end(self):
        if self.tzinfo is not None:
            return self.utc_end.astimezone(self.tzinfo)
        return self.utc_end.replace(tzinfo=None)


class Year(Period):
    def __init__(self, events, date=None, tzinfo=pytz.utc):
        self.tzinfo = self._get_tzinfo(tzinfo)
        if date is None:
            date = timezone.now()
        start, end = self._get_year_range(date)
        super(Year, self).__init__(events, start, end, tzinfo=tzinfo)

    def get_months(self):
        return self.get_periods(Month)

    def next_year(self):
        return Year(self.events, self.end, tzinfo=self.tzinfo)
    next = next_year

    def prev_year(self):
        start = datetime.datetime(self.start.year - 1, self.start.month, self.start.day)
        return Year(self.events, start, tzinfo=self.tzinfo)
    prev = prev_year

    def _get_year_range(self, year):
        #If tzinfo is not none get the local start of the year and convert it to utc.
        naive_start = datetime.datetime(year.year, datetime.datetime.min.month, datetime.datetime.min.day)
        naive_end = datetime.datetime(year.year + 1, datetime.datetime.min.month, datetime.datetime.min.day)

        start = naive_start
        end = naive_end
        if self.tzinfo is not None:
            start = self.tzinfo.localize(naive_start)
            end = self.tzinfo.localize(naive_end)
        return start, end

    def __unicode__(self):
        return str(self.start.year)


class Month(Period):
    """
    The month period has functions for retrieving the week periods within this period
    and day periods within the date.
    """
    def __init__(self, events, date=None, tzinfo=pytz.utc):
        self.tzinfo = self._get_tzinfo(tzinfo)
        if date is None:
            date = timezone.now()
        start, end = self._get_month_range(date)
        super(Month, self).__init__(events, start, end, tzinfo=tzinfo)

    def get_weeks(self):
        return self.get_periods(Week)

    def get_days(self):
        return self.get_periods(Day)

    def get_day(self, daynumber):
        date = self.start
        if daynumber > 1:
            date += datetime.timedelta(days=daynumber - 1)
        return self.create_sub_period(Day, date)

    def next_month(self):
        return Month(self.events, self.end, tzinfo=self.tzinfo)
    next = next_month

    def prev_month(self):
        start = (self.start - datetime.timedelta(days=1)).replace(day=1, tzinfo=self.tzinfo)
        return Month(self.events, start, tzinfo=self.tzinfo)
    prev = prev_month

    def current_year(self):
        return Year(self.events, self.start, tzinfo=self.tzinfo)

    def prev_year(self):
        start = datetime.datetime.min.replace(year=self.start.year - 1, tzinfo=self.tzinfo)
        return Year(self.events, start, tzinfo=self.tzinfo)

    def next_year(self):
        start = datetime.datetime.min.replace(year=self.start.year + 1, tzinfo=self.tzinfo)
        return Year(self.events, start, tzinfo=self.tzinfo)

    def _get_month_range(self, month):
        year = month.year
        month = month.month
        #If tzinfo is not none get the local start of the month and convert it to utc.
        naive_start = datetime.datetime.min.replace(year=year, month=month)
        if month == 12:
            naive_end = datetime.datetime.min.replace(month=1, year=year + 1, day=1)
        else:
            naive_end = datetime.datetime.min.replace(month=month + 1, year=year, day=1)
        start = naive_start
        end = naive_end
        if self.tzinfo is not None:
            start = self.tzinfo.localize(naive_start)
            end = self.tzinfo.localize(naive_end)
        return start, end

    def __unicode__(self):
        return self.name()

    def name(self):
        return standardlib_calendar.month_name[self.start.month]

    def year(self):
        return self.start.year


class Week(Period):
    """
    The Week period that has functions for retrieving Day periods within it
    """
    def __init__(self, events, date=None, tzinfo=pytz.utc):
        self.tzinfo = self._get_tzinfo(tzinfo)
        if date is None:
            date = timezone.now()
        start, end = self._get_week_range(date)
        super(Week, self).__init__(events, start, end, tzinfo=tzinfo)

    def prev_week(self):
        return Week(self.events, self.start - datetime.timedelta(days=7), tzinfo=self.tzinfo)
    prev = prev_week

    def next_week(self):
        return Week(self.events, self.end, tzinfo=self.tzinfo)
    next = next_week

    def current_month(self):
        return Month(self.events, self.start, tzinfo=self.tzinfo)

    def current_year(self):
        return Year(self.events, self.start, tzinfo=self.tzinfo)

    def get_days(self):
        return self.get_periods(Day)

    def _get_week_range(self, week):
        if isinstance(week, datetime.datetime):
            week = week.date()
        # Adjust the start datetime to midnight of the week datetime
        naive_start = datetime.datetime.combine(week, datetime.time.min)

        # Adjust the start datetime to Sunday of the current week
        sub_days = naive_start.isoweekday()
        if sub_days == 7:
            sub_days = 0
        if sub_days > 0:
            naive_start = naive_start - datetime.timedelta(days=sub_days)
        naive_end = naive_start + datetime.timedelta(days=7)

        if self.tzinfo is not None:
            start = self.tzinfo.localize(naive_start)
            end = self.tzinfo.localize(naive_end)
        else:
            start = naive_start
            end = naive_end

        return start, end

    def __unicode__(self):
        date_format = u'l, %s' % ugettext("DATE_FORMAT")
        return ugettext('Week: %(start)s-%(end)s') % {
            'start': date_filter(self.start, date_format),
            'end': date_filter(self.end, date_format),
        }


class Day(Period):
    def __init__(self, events, date=None, tzinfo=pytz.utc):
        self.tzinfo = self._get_tzinfo(tzinfo)
        if date is None:
            date = timezone.now()
        start, end = self._get_day_range(date)
        super(Day, self).__init__(events, start, end, tzinfo=tzinfo)

    def _get_day_range(self, date):
        if isinstance(date, datetime.datetime):
            date = date.date()

        naive_start = datetime.datetime.combine(date, datetime.time.min)
        naive_end = datetime.datetime.combine(date, datetime.time.max)

        if self.tzinfo is not None:
            start = self.tzinfo.localize(naive_start)
            end = self.tzinfo.localize(naive_end)
        else:
            start = naive_start
            end = naive_end
        return start, end

    def __unicode__(self):
        date_format = u'l, %s' % ugettext("DATE_FORMAT")
        return ugettext('Day: %(start)s-%(end)s') % {
            'start': date_filter(self.start, date_format),
            'end': date_filter(self.end, date_format),
        }

    def prev_day(self):
        return Day(self.events, self.start - datetime.timedelta(days=1), tzinfo=self.tzinfo)
    prev = prev_day

    def next_day(self):
        return Day(self.events, self.end + datetime.timedelta(days=1), tzinfo=self.tzinfo)
    next = next_day

    def current_year(self):
        return Year(self.events, self.start, tzinfo=self.tzinfo)

    def current_month(self):
        return Month(self.events, self.start, tzinfo=self.tzinfo)

    def current_week(self):
        return Week(self.events, self.start, tzinfo=self.tzinfo)
