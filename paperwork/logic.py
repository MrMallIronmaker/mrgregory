#from dateutil.relativedelta import relativedelta
import models.deliverables as mrgd
import models.tasks as mrgt
import models.clients as mrgc
import datetime
from itertools import groupby

from django.utils.dateparse import parse_date

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
    if mrgd.Duration(duration) == mrgd.Duration.calendar_day:
        return calculate_calendar_day_offset(date, offset)
    elif mrgd.Duration(duration) == mrgd.Duration.business_day:
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
    try:
        client_info = mrgc.ClientInfo.objects.get(client=client, info_type=citsig)
    except mrgc.ClientInfo.DoesNotExist:
        return None
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
        # then use the review value, 
        # but also if it's got no review do nothing
        if review_deadline is None:
            return
        root_deadline = review_deadline
        root_date = calculate_date_from_deadline(review_deadline, sig_date)
    else:
        # then use the initial value
        root_deadline = final_deadline
        root_date = calculate_final_date(task_status)

    # create the first task.
    root_task = mrgt.Task(
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
        ancestor_task = mrgt.Task.objects.get(
            deadline=ancestor, 
            completed=False,
            task_status=task_status)
        # find date
        date = calculate_date_from_deadline(deadline, ancestor_task.date)
        # create task
        task = mrgt.Task(
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
        for task_status in mrgt.TaskStatus.objects.all():
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

def create_client_info_type(name):
    cit = mrgc.ClientInfoType(title=name)
    cit.save()
    return cit

def all_client_info_types():
    return mrgc.ClientInfoType.objects.all()

def fill_client_info(client, post_dict):
    for cit in all_client_info_types():
        if cit.title in post_dict:
            info = mrgc.ClientInfoDate(client=client, info_type=cit,
                                  date=parse_date(post_dict[cit.title]))
            info.save()

def create_client(post_dict):
    client = mrgc.Client(name=post_dict["name"])
    client.save()
    fill_client_info(client, post_dict)
    return client

def all_clients():
    return mrgc.Client.objects.all()

def all_deliverables():
    return mrgd.Deliverable.objects.all()

def create_deliverable(post_dict):
    # handle the case where I need to make a new client info type
    cit = None
    if post_dict["anchor"] != "other":
        cit = mrgc.ClientInfoType.objects.get(id=post_dict["anchor"])
    else:
        if post_dict["otheranchor"]:
            cit = mrgc.ClientInfoType(title=post_dict["otheranchor"])
            cit.save()

    # handle the case in which I need to make a review item
    if cit is None:
        return None

    final_deadline = mrgd.FinalDeadline(
        relative_info_type=cit,
        offset=time_phrase(
            post_dict["number"],
            post_dict["duration"],
            post_dict["relation"]),
        duration=int(post_dict["duration"]),
        title=post_dict["title"]
    )
    final_deadline.save()
    deliverable = mrgd.Deliverable(title=post_dict["title"], final=final_deadline)
    deliverable.save()
    citsig_title = "signature of " + post_dict["title"]
    citsig = mrgc.ClientInfoTypeSignature(deliverable=deliverable, title=citsig_title)
    citsig.save()

    review_items = ["review_offset", "review_duration"]
    if post_dict["review"] == "1" and \
        all([i in post_dict for i in review_items]):
        review_deadline = mrgd.ReviewDeadline(
            relative_info_type=citsig,
            offset=int(post_dict["review_offset"]),
            duration=int(post_dict["duration"]),
            title="review of " + post_dict["title"]
            )
        review_deadline.save()
        deliverable.review = review_deadline
        deliverable.save()

    return deliverable

def all_durations():
    return [d for d in mrgd.Duration]

def get_deliverable_by_id(deliverable_id):
    return mrgd.Deliverable.objects.get(id=deliverable_id)

def get_step_deadlines_from(deliverable):
    return [i for i in deliverable.step_deadlines.all()]

def get_deadlines_from(deliverable):
    return get_step_deadlines_from(deliverable) + [deliverable.final]

def create_deadline(deliverable, post_dict):
    step_deadline = mrgd.StepDeadline(
        deliverable=deliverable,
        ancestor=mrgd.Deadline.objects.get(id=post_dict["anchor"]),
        offset=time_phrase(
            post_dict["number"],
            post_dict["duration"],
            post_dict["relation"]),
        duration=int(post_dict["duration"]),
        title=post_dict["title"])
    step_deadline.save()

def check_completed_tasks(post_dict):
    for key in post_dict:
        if post_dict[key] == "on":
            task = Task.objects.get(id=int(key))
            task.completed = True
            task.save()

def get_tasks_by_dates():
    all_tasks = [t for t in mrgt.Task.objects.all()]
    get_date = lambda t: t.date
    all_tasks.sort(key=get_date)
    tasks_by_dates = []
    for key, group in groupby(all_tasks, get_date):
        tasks_by_dates.append({
            "date": key,
            "tasks": [t for t in group]
            })
    return tasks_by_dates

def update_task_statuses(post_dict):
    deliverables = all_deliverables()
    clients = all_clients()

    for client in clients:
        for deliverable in deliverables:
            task_status = None
            try:
                task_status = mrgt.TaskStatus.objects.get(client=client, deliverable=deliverable)
            except mrgt.TaskStatus.DoesNotExist:
                task_status = mrgt.TaskStatus(
                    client=client,
                    deliverable=deliverable,
                    needed=False)
            id_string = "c" + str(client.id) + "-d" + str(deliverable.id)
            task_status.needed = id_string in post_dict
            task_status.save()

def get_checked_task_statuses():
    return mrgt.TaskStatus.objects.filter(needed=True)