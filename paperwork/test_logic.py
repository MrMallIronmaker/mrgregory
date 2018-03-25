"""
Test the logic module. At the moment this is just the business day function.
"""
from datetime import datetime
from django.test import TestCase
from paperwork.logic import calculate_business_day_offset

# Create your tests here.

class CalculateBusinessDayTestCase(TestCase):
    """Do the business day calculations take into account the MTWR schedule?"""
    def dates_and_offset(self, src_date_string, dst_date_string, offset):
        """
        Helper function that does most of the work. Really, the interesting parts
        of the function are if it can calculate a business day offset.
        """
        src_date = datetime.strptime(src_date_string, '%y-%m-%d')
        dst_date = datetime.strptime(dst_date_string, '%y-%m-%d')
        test_dst_date = calculate_business_day_offset(src_date, offset)
        self.assertEqual(test_dst_date, dst_date)

    def test_weekday_ahead(self):
        """Sanity check for stepping one day forward."""
        self.dates_and_offset('18-03-06', '18-03-07', 1) # Tuesday and Wednesday

    def test_weekday_behind(self):
        """Sanity check for stepping one day backward."""
        self.dates_and_offset('18-03-06', '18-03-05', -1) # Tuesday and Monday

    def test_weekend_ahead(self):
        """Now things get tricky. One business day after Saturday is Monday."""
        self.dates_and_offset('18-03-10', '18-03-12', 1) # Saturday and Monday

    def test_weekend_behind(self):
        """
        This maybe doesn't make sense, but it's the current convension. One
        business day before Satuday is Wednesday... aka the person has 1 day to
        work after EOD of the due date.
        """
        self.dates_and_offset('18-03-10', '18-03-07', -1) # Saturday and Wednesday

    def test_weekday_ahead_multiple(self):
        """Do weeks work?"""
        self.dates_and_offset('18-03-06', '18-03-21', 9) # Tuesday to Wednesday+2

    def test_weekday_behind_multiple(self):
        """Do weeks work backwards?"""
        self.dates_and_offset('18-03-06', '18-02-22', -6) # Tuesday to Thursday-2

    def test_weekend_ahead_multiple(self):
        """
        Do weeks work when you start on a weekend?
        """
        self.dates_and_offset('18-03-09', '18-03-21', 7) # Friday to Wednesday+2

    def test_weekend_behind_multiple(self):
        """
        Do weeks still work when you start on a weekend and you go backward?
        """
        self.dates_and_offset('18-03-09', '18-02-22', -8) # Friday to Thursday-2
