# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from logic import calculate_business_day_offset
from datetime import datetime

# Create your tests here.

class CalculateBusinessDayTestCase(TestCase):

    def dates_and_offset(self, src_date_string, dst_date_string, offset):
        src_date = datetime.strptime(src_date_string, '%y-%m-%d')
        dst_date = datetime.strptime(dst_date_string, '%y-%m-%d')
        test_dst_date = calculate_business_day_offset(src_date, offset)
        self.assertEqual(test_dst_date, dst_date)

    def test_weekday_ahead(self):
        self.dates_and_offset('18-03-06', '18-03-07', 1) # Tuesday and Wednesday

    def test_weekday_behind(self):
        self.dates_and_offset('18-03-06', '18-03-05', -1) # Tuesday and Monday

    def test_weekend_ahead(self):
        self.dates_and_offset('18-03-10', '18-03-12', 1) # Saturday and Monday

    def test_weekend_behind(self):
        self.dates_and_offset('18-03-10', '18-03-07', -1) # Saturday and Wednesday

    def test_weekday_ahead_multiple(self):
        self.dates_and_offset('18-03-06', '18-03-21', 9) # Tuesday to Wednesday+2

    def test_weekday_behind_multiple(self):
        self.dates_and_offset('18-03-06', '18-02-22', -6) # Tuesday to Thursday-2

    def test_weekend_ahead_multiple(self):
        self.dates_and_offset('18-03-09', '18-03-21', 7) # Friday to Wednesday+2

    def test_weekend_behind_multiple(self):
        self.dates_and_offset('18-03-09', '18-02-22', -8) # Friday to Thursday-2