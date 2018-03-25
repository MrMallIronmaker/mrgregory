"""
Handling the URL requests views relating to tasks
"""

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from paperwork import logic

@login_required
def view_tasks(request):
    logic.create_tasks()
    tasks_by_dates = logic.get_tasks_by_dates()
    return render(request, 'paperwork/tasks.html', {
        "tasks_by_dates" : tasks_by_dates,
        "other_link" : "/completed_tasks/"
    })

@login_required
def completed_tasks(request):
    logic.create_tasks()
    tasks_by_dates = logic.get_completed_tasks_by_dates()
    return render(request, 'paperwork/tasks.html', {
        "tasks_by_dates" : tasks_by_dates,
        "other_link" : "/tasks/"
    })

@login_required
def complete_task(request, task_id):
    if request.method == "POST":
        print request.POST
        logic.update_completed_tasks({
            "completed" : int(task_id)
            })

    return HttpResponseRedirect(request.POST["from"])

@login_required
def uncomplete_task(request, task_id):
    # TODO: refactor in this with complete_task
    if request.method == "POST":
        print request.POST
        logic.update_completed_tasks({
            "uncompleted" : int(task_id)
            })

    return HttpResponseRedirect(request.POST["from"])

@login_required
def dpc(request):
    # if it's a post, update the task statuses
    if request.method == "POST":
        logic.update_task_statuses(request.POST)
    task_statuses = logic.get_checked_task_statuses()

    return render(request, 'paperwork/deliverables_per_client.html', {
        "deliverables" : logic.all_deliverables(),
        "clients" : logic.all_clients(),
        "task_statuses" : task_statuses,
    })

@login_required
def make_tasks(_):
    logic.create_tasks()
    return HttpResponseRedirect("/tasks/")
