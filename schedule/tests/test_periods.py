import datetime
import pytz

from django.test import TestCase

from schedule.conf.settings import FIRST_DAY_OF_WEEK
from schedule.models import Event, Calendar
from schedule.periods import Period, Month, Day, Year, Week

class TestPeriod(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']

    def setUp(self):
        self.events = Event.objects.filter(calendar__pk=2)
        self.period = Period(events=self.events,
                            start = datetime.datetime(2014, 1, 4, 7, 0, tzinfo=pytz.utc),
                            end = datetime.datetime(2016, 1, 21, 7, 0, tzinfo=pytz.utc))

    def test_get_events(self):
        event_list = self.period.events
        self.assertEqual(["%s to %s" %(e.show.date.start, e.show.date.end) for e in event_list],
                ['2015-02-10 09:00:00+00:00 to 2015-02-10 09:00:00+00:00',
                    '2015-02-11 09:00:00+00:00 to 2015-02-11 09:00:00+00:00',
                    '2015-02-10 10:30:00+00:00 to 2015-02-10 10:30:00+00:00'])

    def test_get_event_partials(self):
        event_dicts = self.period.get_event_partials()
        self.assertEqual(set(event_dicts), set(self.events))


class TestYear(TestCase):

    def setUp(self):
        self.year = Year(events=[], date=datetime.datetime(2008, 4, 1, tzinfo=pytz.utc))

    def test_get_months(self):
        months = self.year.get_months()
        self.assertEqual([month.start for month in months],
            [datetime.datetime(2008, i, 1, tzinfo=pytz.utc) for i in range(1,13)])


class TestMonth(TestCase):

    def setUp(self):
        self.month = Month(events=Event.objects.all(),
                           date=datetime.datetime(2008, 2, 7, 9, 0, tzinfo=pytz.utc))

    def test_get_weeks(self):
        weeks = self.month.get_weeks()
        actuals = [(week.start, week.end) for week in weeks]

        expecteds = [
            (datetime.datetime(2008, 1, 27, 0, 0, tzinfo=pytz.utc),
             datetime.datetime(2008, 2, 3, 0, 0, tzinfo=pytz.utc)),
            (datetime.datetime(2008, 2, 3, 0, 0, tzinfo=pytz.utc),
             datetime.datetime(2008, 2, 10, 0, 0, tzinfo=pytz.utc)),
            (datetime.datetime(2008, 2, 10, 0, 0, tzinfo=pytz.utc),
             datetime.datetime(2008, 2, 17, 0, 0, tzinfo=pytz.utc)),
            (datetime.datetime(2008, 2, 17, 0, 0, tzinfo=pytz.utc),
             datetime.datetime(2008, 2, 24, 0, 0, tzinfo=pytz.utc)),
            (datetime.datetime(2008, 2, 24, 0, 0, tzinfo=pytz.utc),
             datetime.datetime(2008, 3, 2, 0, 0, tzinfo=pytz.utc))
        ]

        for actual, expected in zip(actuals, expecteds):
            self.assertEqual(actual, expected)

    def test_get_days(self):
        weeks = self.month.get_weeks()
        week = list(weeks)[0]
        days = week.get_days()
        actuals = [(len(day.events), day.start,day.end) for day in days]
        expecteds = [
            (
                0,
                datetime.datetime(2008, 1, 27, 0, 0, tzinfo=pytz.utc),
                datetime.datetime(2008, 1, 27, 23, 59, 59, 999999, tzinfo=pytz.utc)
            ),
            (
                0,
                datetime.datetime(2008, 1, 28, 0, 0, tzinfo=pytz.utc),
                datetime.datetime(2008, 1, 28, 23, 59, 59, 999999, tzinfo=pytz.utc)
            ),
            (
                0,
                datetime.datetime(2008, 1, 29, 0, 0, tzinfo=pytz.utc),
                datetime.datetime(2008, 1, 29, 23, 59, 59, 999999, tzinfo=pytz.utc)
            ),
            (
                0,
                datetime.datetime(2008, 1, 30, 0, 0, tzinfo=pytz.utc),
                datetime.datetime(2008, 1, 30, 23, 59, 59, 999999, tzinfo=pytz.utc)
            ),
            (
                0,
                datetime.datetime(2008, 1, 31, 0, 0, tzinfo=pytz.utc),
                datetime.datetime(2008, 1, 31, 23, 59, 59, 999999, tzinfo=pytz.utc)
            ),
            (
                0,
                datetime.datetime(2008, 2, 1, 0, 0, tzinfo=pytz.utc),
                datetime.datetime(2008, 2, 1, 23, 59, 59, 999999, tzinfo=pytz.utc)
            ),
            (
                0,
                datetime.datetime(2008, 2, 2, 0, 0, tzinfo=pytz.utc),
                datetime.datetime(2008, 2, 2, 23, 59, 59, 999999, tzinfo=pytz.utc)
            ),
        ]

        for actual, expected in zip(actuals, expecteds):
            self.assertEqual(actual, expected)


    def test_month_convenience_functions(self):
        self.assertEqual( self.month.prev_month().start, datetime.datetime(2008, 1, 1, 0, 0, tzinfo=pytz.utc))
        self.assertEqual( self.month.next_month().start, datetime.datetime(2008, 3, 1, 0, 0, tzinfo=pytz.utc))
        self.assertEqual( self.month.current_year().start, datetime.datetime(2008, 1, 1, 0, 0, tzinfo=pytz.utc))
        self.assertEqual( self.month.prev_year().start, datetime.datetime(2007, 1, 1, 0, 0, tzinfo=pytz.utc))
        self.assertEqual( self.month.next_year().start, datetime.datetime(2009, 1, 1, 0, 0, tzinfo=pytz.utc))


class TestDay(TestCase):
    def setUp(self):
        self.day = Day(events=Event.objects.all(),
                           date=datetime.datetime(2008, 2, 7, 9, 0, tzinfo=pytz.utc))

    def test_day_setup(self):
        self.assertEqual( self.day.start, datetime.datetime(2008, 2, 7, 0, 0, tzinfo=pytz.utc))
        self.assertEqual( self.day.end, datetime.datetime(2008, 2, 7, 23, 59, 59, 999999, tzinfo=pytz.utc))

    def test_day_convenience_functions(self):
        self.assertEqual( self.day.prev_day().start, datetime.datetime(2008, 2, 6, 0, 0, tzinfo=pytz.utc))
        self.assertEqual( self.day.next_day().start, datetime.datetime(2008, 2, 8, 0, 0, tzinfo=pytz.utc))

    def test_time_slot(self):
        slot_start = datetime.datetime(2008, 2, 7, 13, 30, tzinfo=pytz.utc)
        slot_end = datetime.datetime(2008, 2, 7, 15, 0, tzinfo=pytz.utc)
        period = self.day.get_time_slot( slot_start, slot_end )
        self.assertEqual( period.start, slot_start )
        self.assertEqual( period.end, slot_end )


class TestAwareDay(TestCase):
    fixtures = ['users', 'contactInfos', 'contacts', 'locations', 'zipcodes', 'profiles',
                 'applications', 'publicRequests', 'numApplicants',
                'threads', 'messages', 'participants', 'dates', 'genres',
                'albums', 'artists', 'tracks', 'media', 'calendars', 'info',
                'shows', 'events']

    def setUp(self):
        self.event = Event.objects.get(pk=2)
        self.timezone = pytz.timezone('Europe/Amsterdam')

        self.event.show.date.start = self.timezone.localize(datetime.datetime(2008, 2, 7, 0, 20))
        self.event.show.date.end = self.timezone.localize(datetime.datetime(2008, 2, 7, 0, 21))
        self.event.show.date.save()

        self.day = Day(
            events=[self.event,],
            date=self.timezone.localize(datetime.datetime(2008, 2, 7, 9, 0)),
            tzinfo=self.timezone,
        )

    def test_day_range(self):
        # TODO: fix this
        pass
        """start = datetime.datetime(2008, 2, 6, 23, 0, tzinfo=pytz.utc)
        end = datetime.datetime(2008, 2, 7, 23, 59, 59, 999999, tzinfo=pytz.utc)

        self.assertEqual(start, self.day.start)
        self.assertEqual(end, self.day.end)"""

    def test_event(self):
        self.assertEqual(self.event in [event for event in self.day.events], True)


class TestTzInfoPersistence(TestCase):
    def setUp(self):
        self.timezone = pytz.timezone('Europe/Amsterdam')
        self.day = Day(
            events=Event.objects.all(),
            date=self.timezone.localize(datetime.datetime(2013, 12, 17, 9, 0)),
            tzinfo=self.timezone
        )

        self.week = Week(
            events=Event.objects.all(),
            date=self.timezone.localize(datetime.datetime(2013, 12, 17, 9, 0)),
            tzinfo=self.timezone,
        )

        self.month = Month(
            events=Event.objects.all(),
            date=self.timezone.localize(datetime.datetime(2013, 12, 17, 9, 0)),
            tzinfo=self.timezone,
        )

        self.year = Year(
            events=Event.objects.all(),
            date=self.timezone.localize(datetime.datetime(2013, 12, 17, 9, 0)),
            tzinfo=self.timezone,
        )

    def test_persistence(self):
        self.assertEqual(self.day.tzinfo, self.timezone)
        self.assertEqual(self.week.tzinfo, self.timezone)
        self.assertEqual(self.month.tzinfo, self.timezone)
        self.assertEqual(self.year.tzinfo, self.timezone)


class TestAwareWeek(TestCase):
    def setUp(self):
        self.timezone = pytz.timezone('Europe/Amsterdam')
        self.week = Week(
            events=Event.objects.all(),
            date=self.timezone.localize(datetime.datetime(2013, 12, 17, 9, 0)),
            tzinfo=self.timezone,
        )

    def test_week_range(self):
        start = self.timezone.localize(datetime.datetime(2013, 12, 15, 0, 0))
        end = self.timezone.localize(datetime.datetime(2013, 12, 22, 0, 0))

        self.assertEqual(self.week.tzinfo, self.timezone)
        self.assertEqual(start, self.week.start)
        self.assertEqual(end, self.week.end)


class TestAwareMonth(TestCase):
    def setUp(self):
        self.timezone = pytz.timezone('Europe/Amsterdam')
        self.month = Month(
            events=Event.objects.all(),
            date=self.timezone.localize(datetime.datetime(2013, 11, 17, 9, 0)),
            tzinfo=self.timezone,
        )

    def test_month_range(self):
        start = self.timezone.localize(datetime.datetime(2013, 11, 1, 0, 0))
        end = self.timezone.localize(datetime.datetime(2013, 12, 1, 0, 0))

        self.assertEqual(self.month.tzinfo, self.timezone)
        self.assertEqual(start, self.month.start)
        self.assertEqual(end, self.month.end)


class TestAwareYear(TestCase):
    def setUp(self):
        self.timezone = pytz.timezone('Europe/Amsterdam')
        self.year = Year(
            events=Event.objects.all(),
            date=self.timezone.localize(datetime.datetime(2013, 12, 17, 9, 0)),
            tzinfo=self.timezone,
        )

    def test_year_range(self):
        start = self.timezone.localize(datetime.datetime(2013, 1, 1, 0, 0))
        end = self.timezone.localize(datetime.datetime(2014, 1, 1, 0, 0))

        self.assertEqual(self.year.tzinfo, self.timezone)
        self.assertEqual(start, self.year.start)
        self.assertEqual(end, self.year.end)

class TestStrftimeRefactor(TestCase):
    """
        Test for the refactor of strftime
    """
    def test_years_before_1900(self):
        d = datetime.date(year=1899, month=1, day=1)
        m = Month([], d)
        try:
            m.name()
        except ValueError as value_error:
            self.fail(value_error)
