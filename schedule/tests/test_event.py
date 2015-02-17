import datetime
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
import pytz

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from schedule.models import Event, Calendar


class TestEvent(TestCase):

    def setUp(self):
        cal = Calendar(name="MyCal")
        cal.save()

    def __create_event(self, title, start, end, cal):
        return Event(**{
                'title': title,
                'start': start,
                'end': end,
                'calendar': cal
               })

    def test_edge_case_events(self):
        cal = Calendar(name="MyCal")
        cal.save()
        data_1 = {
            'title': 'Edge case event test one',
            'start': datetime.datetime(2013, 1, 5, 8, 0, tzinfo=pytz.utc),
            'end': datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
            'calendar': cal
        }
        data_2 = {
            'title': 'Edge case event test two',
            'start': datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
            'end': datetime.datetime(2013, 1, 5, 12, 0, tzinfo=pytz.utc),
            'calendar': cal
        }
        event_one = Event(**data_1)
        event_two = Event(**data_2)
        event_one.save()
        event_two.save()
        occurrences_two = event_two.get_occurrences(datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
                                                    datetime.datetime(2013, 1, 5, 12, 0, tzinfo=pytz.utc))
        self.assertEquals(1, len(occurrences_two))

        occurrences_one = event_one.get_occurrences(datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
                                                    datetime.datetime(2013, 1, 5, 12, 0, tzinfo=pytz.utc))
        self.assertEquals(0, len(occurrences_one))



    def test_event_get_occurrences_after(self):

        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()

        recurring_event = self.__create_recurring_event(
                    'Recurrent event test get_occurrence',
                    datetime.datetime(2008, 1, 5, 8, 0, tzinfo=pytz.utc),
                    datetime.datetime(2008, 1, 5, 9, 0, tzinfo=pytz.utc),
                    datetime.datetime(2008, 5, 5, 0, 0, tzinfo=pytz.utc),
                    rule,
                    cal,
                    )
        event_one = self.__create_event(
                'Edge case event test one',
                datetime.datetime(2013, 1, 5, 8, 0, tzinfo=pytz.utc),
                datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
                cal
               )
        event_two = self.__create_event(
                'Edge case event test two',
                datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
                datetime.datetime(2013, 1, 5, 12, 0, tzinfo=pytz.utc),
                cal
               )
        event_one.save()
        event_two.save()
        occurrences_two = event_two.get_occurrences(
                                    datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
                                    datetime.datetime(2013, 1, 5, 12, 0, tzinfo=pytz.utc))

        self.assertEquals(1, len(occurrences_two))

        occurrences_one = event_one.get_occurrences(
                                    datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
                                    datetime.datetime(2013, 1, 5, 12, 0, tzinfo=pytz.utc))

        self.assertEquals(0, len(occurrences_one))


    def test_prevent_type_error_when_comparing_naive_and_aware_dates(self):
        # this only test if the TypeError is raised
        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency = "WEEKLY")
        rule.save()

        event = self.__create_recurring_event(
                    'Recurrent event test get_occurrence',
                    datetime.datetime(2008, 1, 5, 8, 0, tzinfo=pytz.utc),
                    datetime.datetime(2008, 1, 5, 9, 0, tzinfo=pytz.utc),
                    datetime.datetime(2008, 5, 5, 0, 0, tzinfo=pytz.utc),
                    rule,
                    cal,
                    )
        naive_date = datetime.datetime(2008, 1, 20, 0, 0)
        self.assertIsNone(event.get_occurrence(naive_date))

    @override_settings(USE_TZ=False)
    def test_prevent_type_error_when_comparing_dates_when_tz_off(self):
        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency = "WEEKLY")
        rule.save()

        event = self.__create_recurring_event(
                    'Recurrent event test get_occurrence',
                    datetime.datetime(2008, 1, 5, 8, 0),
                    datetime.datetime(2008, 1, 5, 9, 0),
                    datetime.datetime(2008, 5, 5, 0, 0),
                    rule,
                    cal,
                    )
        naive_date = datetime.datetime(2008, 1, 20, 0, 0)
        self.assertIsNone(event.get_occurrence(naive_date))

    def test_get_for_object(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        event_relations = list(Event.objects.get_for_object(user, 'owner', inherit=False))
        self.assertEquals(len(event_relations), 0)

        rule = Rule(frequency = "DAILY")
        rule.save()
        cal = Calendar(name='MyCal')
        cal.save()
        event = self.__create_event(
                'event test',
                datetime.datetime(2013, 1, 5, 8, 0, tzinfo=pytz.utc),
                datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
                cal
               )
        event.save()
        events = list(Event.objects.get_for_object(user, 'owner', inherit=False))
        self.assertEquals(len(events), 0)
        EventRelation.objects.create_relation(event, user, 'owner')

        events = list(Event.objects.get_for_object(user, 'owner', inherit=False))
        self.assertEquals(len(events), 1)
        self.assertEquals(event, events[0])

    def test_get_absolute(self):
        cal = Calendar(name='MyCal')
        cal.save()
        rule = Rule(frequency = "DAILY")
        rule.save()
        start = timezone.now() + datetime.timedelta(days=1)
        event = self.__create_recurring_event(
                            'Non recurring event test get_occurrence',
                            start,
                            start + datetime.timedelta(hours=1),
                            start + datetime.timedelta(days=10),
                            rule,
                            cal)
        event.save()
        url = event.get_absolute_url()
        self.assertEquals(reverse('event', kwargs={'event_id': event.id}), url)

    def test_(self):
        pass
