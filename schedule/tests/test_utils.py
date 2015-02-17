import os
import pytz
import datetime

from django.test import TestCase
from django.utils import timezone

from schedule.models import Calendar


class TestEventListManager(TestCase):
    def setUp(self):
        cal = Calendar.objects.create(name="MyCal")
        self.default_tzinfo = timezone.get_default_timezone()
