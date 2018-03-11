#from dateutil.relativedelta import relativedelta
from models.deliverables import Duration
from models.tasks import TaskStatus, Task
from models.clients import ClientInfo
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
	if Duration(duration) == Duration.calendar_day:
		return calculate_calendar_day_offset(date, offset)
	elif Duration(duration) == Duration.business_day:
		return calculate_business_day_offset(date, offset)
	else:
		raise ValueError("Duration not implemented.")

def calculate_date_from_deadline(deadline, old_date):
	return calculate_date(old_date, deadline.offset, deadline.duration)

def get_signature_date(client, citsig):
	try:
		citsig = citsig.clientinfotype_ptr
	except AttributeError:
		pass

	client_info = ClientInfo.objects.get(client=client, info_type=citsig)
	return client_info.clientinfodate.date

def calculate_final_date(task_status):
	final_deadline = task_status.deliverable.final
	client = task_status.client
	fd_rit = final_deadline.relative_info_type
	sig_date = get_signature_date(client, fd_rit)
	return calculate_date(sig_date, final_deadline.offset, final_deadline.duration)

def get_signature_date_from_task_status(task_status):
	client = task_status.client
	citsig = task_status.deliverable.clientinfotypesignature
	return get_signature_date(client, citsig)

def add_dates(task_status):
	# Is it the final or the review?
	sig_date = get_signature_date_from_task_status(task_status)
	root_deadline = None
	root_date = None
	final_deadline = task_status.deliverable.final
	review_deadline = task_status.deliverable.review

	# if there is a signature date,
	if sig_date:
		# then use the review value
		root_deadline = review_deadline
		root_date = calculate_date_from_deadline(review_deadline, sig_date)
	else:
		# then use the initial value
		root_deadline = final_deadline
		root_date = calculate_final_date(task_status)

	# create the first task.
	root_task = Task(
		task_status=task_status,
		deadline=root_deadline,
		date=root_date,
		completed=False)
	root_task.save()

	# create list
	# right now, only the final has children
	deadlines = [d for d in final_deadline.children.all()]
	# while list is non-empty
	while deadlines:
		# grab one,
		deadline = deadlines.pop()
		# get ancestor
		ancestor = deadline.ancestor
		if ancestor == final_deadline and sig_date:
			ancestor = review_deadline
		ancestor_task = Task.objects.get(
			deadline=ancestor, 
			completed=False,
			task_status=task_status)
		# find date
		date = calculate_date_from_deadline(deadline, ancestor_task.date)
		# create task
		task = Task(
			task_status=task_status,
			deadline=deadline,
			date=date,
			completed=False)
		task.save()
		deadlines += [d for d in deadline.children.all()]

def is_dateable(task_status):
	#TODO: don't lie
	return True

def create_tasks():
	#TODO: I need better names for these variables
	undated_items = True
	dated_items = set({})
	while undated_items:
		undated_items = False
		for task_status in TaskStatus.objects.all():
			if not task_status.needed:
				continue
			# if it's been dated
			if task_status in dated_items:
				continue
			# if you can date it
			if is_dateable(task_status):
				add_dates(task_status)
				dated_items.add(task_status)
			else:
				undated_items = True

