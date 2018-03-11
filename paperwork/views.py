# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from itertools import groupby

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from paperwork.models import ClientInfoType, Client, ClientInfoDate, \
    Deliverable, Deadline, FinalDeadline, StepDeadline, Duration, \
    ClientInfoTypeSignature, ReviewDeadline, TaskStatus, Task
import paperwork.logic

# Create your views here.

def home(request):
    return render(request, 'paperwork/home.html')

def login_page(request):
    if request.method == "POST":
        # Auto login the user
        username = request.POST["username"]
        password = request.POST["password"]
        a_u = authenticate(username=username, password=password)
        if a_u is not None:
            if a_u.is_active:
                login(request, a_u)
                next_url = '/'
                if "next" in request.GET:
                    next_url = request.GET["next"]
                return HttpResponseRedirect(next_url)
        else:
            return HttpResponseRedirect('/login/')

    next_url = '/'
    if "next" in request.GET:
        next_url = request.GET["next"]
    return render(request, 'paperwork/login.html', {
        "next" : next_url
        })


@login_required
def client_info_types(request):
    # does the request have a post option?
    # if so, add it to the database.
    if "name" in request.POST:
        name = request.POST["name"]
        cit = ClientInfoType(title=name)
        cit.save()

    return render(request, 'paperwork/client_info_types.html', {
        'client_info_type_list' : ClientInfoType.objects.all()
    })

@login_required
def clients(request):
    # does the request have a post option?
    # if so, add it to the database.
    if "name" in request.POST:
        name = request.POST["name"]

        # ok, so make that client
        client = Client(name=name)
        client.save()

        for cit in ClientInfoType.objects.all():
            if cit.title in request.POST:
                info = ClientInfoDate(client=client, info_type=cit,
                                      date=parse_date(request.POST[cit.title]))
                info.save()

    return render(request, 'paperwork/clients.html', {
        'client_info_type_list' : ClientInfoType.objects.all(),
        'client_list' : Client.objects.all(),
    })

@login_required
def deliverables(request):

    return render(request, 'paperwork/deliverables.html', {
        'deliverable_list' : Deliverable.objects.all()
    })

@login_required
def new_deliverable(request):
    # if there's a POST, process it and redirect.
    required_post_items = ["title", "anchor", "number", "duration", \
    "relation", "review"]
    if all([i in request.POST for i in required_post_items]):
        # handle the case where I need to make a new client info type
        cit = None
        if request.POST["anchor"] != "other":
            cit = ClientInfoType.objects.get(id=request.POST["anchor"])
        else:
            if request.POST["otheranchor"]:
                cit = ClientInfoType(title=request.POST["otheranchor"])
                cit.save()

        # handle the case in which I need to make a review item

        if cit:
            final_deadline = FinalDeadline(
                relative_info_type=cit,
                offset=paperwork.logic.time_phrase(
                    request.POST["number"],
                    request.POST["duration"],
                    request.POST["relation"]),
                duration=int(request.POST["duration"]),
                title=request.POST["title"]
            )
            final_deadline.save()
            deliverable = Deliverable(title=request.POST["title"], final=final_deadline)
            deliverable.save()
            citsig_title = "signature of " + request.POST["title"]
            citsig = ClientInfoTypeSignature(deliverable=deliverable, title=citsig_title)
            citsig.save()

            review_items = ["review_offset", "review_duration"]
            if request.POST["review"] == "1" and \
                all([i in request.POST for i in review_items]):
                review_deadline = ReviewDeadline(
                    relative_info_type=citsig,
                    offset=int(request.POST["review_offset"]),
                    duration=int(request.POST["duration"]),
                    title="review of " + request.POST["title"]
                    )
                review_deadline.save()
                deliverable.review = review_deadline
                deliverable.save()


            return HttpResponseRedirect(reverse('paperwork:deliverable', args=(deliverable.id,)))

    # if there's no POST, then just go ahead and display the page.
    return render(request, 'paperwork/new_deliverable.html', {
        'client_info_type_list' : ClientInfoType.objects.all(),
        'duration' : [d for d in Duration],
    })

@login_required
def view_deliverable(request, deliverable_id):
    # setup
    deliverable = Deliverable.objects.get(id=deliverable_id)
    step_deadlines = [i for i in deliverable.step_deadlines.all()]
    deadlines = [i for i in step_deadlines] + [deliverable.final]
    duration = [d for d in Duration]

    # if valid POST:
    if all([i in request.POST for i in ["title", "anchor", "number", "duration", "relation"]]):
        step_deadline = StepDeadline(
            deliverable=deliverable,
            ancestor=Deadline.objects.get(id=request.POST["anchor"]),
            offset=paperwork.logic.time_phrase(
                request.POST["number"],
                request.POST["duration"],
                request.POST["relation"]),
            duration=int(request.POST["duration"]),
            title=request.POST["title"])
        step_deadline.save()
        deadlines += [step_deadline]
        step_deadlines += [step_deadline]

    return render(request, 'paperwork/deliverable.html', {
        "dl" : deliverable,
        "step_deadlines" : step_deadlines,
        "deadlines" : deadlines,
        "duration" : duration
    })

@login_required
def tasks(request):
    if request.method == "POST":
        for key in request.POST:
            if request.POST[key] == "on":
                task = Task.objects.get(id=int(key))
                task.completed = True
                task.save()

    all_tasks = [t for t in Task.objects.all()]
    get_date = lambda t: t.date
    all_tasks.sort(key=get_date)
    tasks_by_dates = []
    for key, group in groupby(all_tasks, get_date):
        tasks_by_dates.append({
            "date": key,
            "tasks": [t for t in group]
            })
    return render(request, 'paperwork/tasks.html', {
        "tasks_by_dates" : tasks_by_dates
    })

@login_required
def dpc(request):
    deliverables = [d for d in Deliverable.objects.all()]
    clients = [c for c in Client.objects.all()]
    # if it's a post, update the task statuses
    if request.method == "POST":
        for client in clients:
            for deliverable in deliverables:
                task_status = None
                try:
                    task_status = TaskStatus.objects.get(client=client, deliverable=deliverable)
                except TaskStatus.DoesNotExist:
                    task_status = TaskStatus(
                        client=client,
                        deliverable=deliverable,
                        needed=False)
                id_string = "c" + str(client.id) + "-d" + str(deliverable.id)
                task_status.needed = id_string in request.POST
                task_status.save()

    # produce the task_status dictionary:
    # accessed like task_status[client][deliverable]
    task_statuses = TaskStatus.objects.filter(needed=True)

    return render(request, 'paperwork/deliverables_per_client.html', {
        "deliverables" : deliverables,
        "clients" : clients,
        "task_statuses" : task_statuses,
    })

@login_required
def make_tasks(request):
    paperwork.logic.create_tasks()
    return HttpResponseRedirect("/tasks/")