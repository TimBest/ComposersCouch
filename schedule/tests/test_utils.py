import datetime

from django.test import TestCase
from django.utils import timezone

from schedule.utils import coerce_date_dict


class TestViewUtils(TestCase):
    """def test_check_next_url(self):
        url = "http://thauber.com"
        self.assertTrue(check_next_url(url) is None)
        url = "/hello/world/"
        self.assertEqual(url, check_next_url(url))"""

    def test_coerce_date_dict(self):
        self.assertEqual(
            coerce_date_dict({'year': '2008', 'month': '4', 'day': '2', 'hour': '4', 'minute': '4'}),
            datetime.datetime(year=2008, month=4, day=2, hour=4, minute=4)
        )

    def test_coerce_date_dict_partial(self):
        self.assertEqual(
            coerce_date_dict({'year': '2008', 'month': '4', 'day': '2'}),
            datetime.datetime(year=2008, month=4, day=2)
        )

    def test_coerce_date_dict_empty(self):
        # empty dictionary returns current datetime
        before = timezone.now()
        current = coerce_date_dict({})
        after = timezone.now()
        self.assertTrue(before < current)
        self.assertTrue(current < after)

    def test_coerce_date_dict_missing_values(self):
        # test defaulting on missing value
        self.assertEqual(
            coerce_date_dict({'year': '2008', 'month': '4', 'hours': '3'}),
            datetime.datetime(year=2008, month=4, day=1)
        )
