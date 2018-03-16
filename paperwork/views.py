# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from itertools import groupby

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from paperwork import logic

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
        logic.create_client_info_type(name=name)

    return render(request, 'paperwork/client_info_types.html', {
        'client_info_type_list' : logic.all_client_info_types()
    })

@login_required
def clients(request):
    # does the request have a post option?
    # if so, add it to the database.
    if "name" in request.POST:
        name = request.POST["name"]
        logic.create_client(request.POST)

    return render(request, 'paperwork/clients.html', {
        'client_info_type_list' : logic.all_client_info_types(),
        'client_list' : logic.all_clients(),
    })

@login_required
def deliverables(request):

    return render(request, 'paperwork/deliverables.html', {
        'deliverable_list' : logic.all_deliverables()
    })

@login_required
def new_deliverable(request):
    # if there's a POST, process it and redirect.
    required_post_items = ["title", "anchor", "number", "duration", \
    "relation", "review"]
    if all([i in request.POST for i in required_post_items]):
        deliverable = logic.create_deliverable(request.POST)
        if deliverable:
            return HttpResponseRedirect(reverse('paperwork:deliverable', args=(deliverable.id,)))

    # if there's no POST, then just go ahead and display the page.
    return render(request, 'paperwork/new_deliverable.html', {
        'client_info_type_list' : logic.all_client_info_types(),
        'duration' : logic.all_durations(),
    })

@login_required
def view_deliverable(request, deliverable_id):
    # setup
    deliverable = logic.get_deliverable_by_id(deliverable_id)

    # if valid POST:
    if all([i in request.POST for i in ["title", "anchor", "number", "duration", "relation"]]):
        create_deadline(deliverable, request.POST)

    return render(request, 'paperwork/deliverable.html', {
        "dl" : deliverable,
        "step_deadlines" : logic.get_step_deadlines_from(deliverable),
        "deadlines" : logic.get_deadlines_from(deliverable),
        "duration" : logic.all_durations()
    })

@login_required
def tasks(request):
    if request.method == "POST":
        logic.check_completed_tasks(request.POST)

    tasks_by_dates = logic.get_tasks_by_dates()
    return render(request, 'paperwork/tasks.html', {
        "tasks_by_dates" : tasks_by_dates
    })

@login_required
def dpc(request):
    # if it's a post, update the task statuses
    if request.method == "POST":
        update_task_statuses(request.POST)
    task_statuses = logic.get_checked_task_statuses()

    return render(request, 'paperwork/deliverables_per_client.html', {
        "deliverables" : logic.all_deliverables(),
        "clients" : logic.all_clients(),
        "task_statuses" : task_statuses,
    })

@login_required
def make_tasks(request):
    logic.create_tasks()
    return HttpResponseRedirect("/tasks/")