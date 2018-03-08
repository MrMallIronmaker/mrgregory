#from dateutil.relativedelta import relativedelta
from models.deliverables import DURATION_CHOICES
import datetime

def time_phrase(number, duration, relation):
	# assume duration is days
	if relation == "after":
		direction = 1
	elif relation == "before":
		direction = -1
	return int(number) * direction

def calculate_calendar_day_offset(date, offset):
	return date + datetime.timedelta(offset)

def check_as_work_day(date):
	return date.weekday() in [0, 1, 2, 3] # M T W R

def calculate_business_day_offset(date, offset):
	# in the future, call into an availability calendar.

	# on a M T W R schedule, four business days is a week.
	weeks = (offset - 1) / 4
	days_from_week = weeks * 4
	day_difference = offset - days_from_week
	approximate_date = date + datetime.timedelta(days=weeks*7)
	while day_difference > 0:
		approximate_date = approximate_date + datetime.timedelta(days=1)
		if check_as_work_day(approximate_date):
			day_difference -= 1
	return approximate_date


def calculate_date(date, offset, duration):
	if duration == DURATION_CHOICES.calendar_day:
		return calculate_calendar_day_offset(date, offset)
	elif duration == DURATION_CHOICES.business_day:
		return calculate_business_day_offset(date, offset)
