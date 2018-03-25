from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from paperwork import logic

@login_required
def view_deliverables(request):
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
            return HttpResponseRedirect(
                reverse('paperwork:deliverable',
                        args=(deliverable.id,)))

    # if there's no POST, then just go ahead and display the page.
    return render(request, 'paperwork/new_deliverable.html', {
        'client_info_type_list' : logic.all_client_info_types(),
        'duration' : logic.all_durations(),
    })

@login_required
def view_deliverable(request, deliverable_id):
    # setup
    deliverable = logic.get_deliverable_by_id(deliverable_id)

    return render(request, 'paperwork/deliverable.html', {
        "dl" : deliverable,
        "step_deadlines" : logic.get_step_deadlines_from(deliverable),
        "deadlines" : logic.get_deadlines_from(deliverable),
        "duration" : logic.all_durations()
    })

@login_required
def new_deadline(request, deliverable_id):
    # setup
    deliverable = logic.get_deliverable_by_id(deliverable_id)

    # if valid POST:
    deadline_reqs = ["title", "anchor", "number", "duration", "relation"]
    if all(["nd-" + i in request.POST for i in deadline_reqs]):
        useful_dict = {}
        for name in deadline_reqs:
            useful_dict[name] = request.POST["nd-" + name]
        logic.create_deadline(deliverable, useful_dict)

    return HttpResponseRedirect(reverse('paperwork:deliverable',
                                        args=(deliverable.id,)))

@login_required
def edit_deadline(request, deliverable_id, deadline_id):

    deliverable = logic.get_deliverable_by_id(deliverable_id)

    deadline_reqs = ["title", "anchor", "number", "duration", "relation"]

    prefix = "sd-" + str(deadline_id) + "-"

    if all([prefix + i in request.POST for i in deadline_reqs]):
        useful_dict = {}
        for name in deadline_reqs:
            useful_dict[name] = request.POST[prefix + name]
        logic.update_deadline(int(deadline_id), useful_dict)

    return HttpResponseRedirect(reverse('paperwork:deliverable',
                                        args=(deliverable.id,)))

@login_required
def edit_deliverable(request, deliverable_id):
    # if there's a POST, process it and redirect.
    deliverable = logic.get_deliverable_by_id(deliverable_id)

    required_post_items = ["title", "anchor", "number", "duration", \
    "relation", "review"]
    if all([i in request.POST for i in required_post_items]):
        deliverable = logic.update_deliverable(deliverable, request.POST)
        if deliverable:
            return HttpResponseRedirect(
                reverse('paperwork:deliverable',
                        args=(deliverable.id,)))

    # if there's no POST, then just go ahead and display the page.
    return render(request, 'paperwork/edit_deliverable.html', {
        'client_info_type_list' : logic.all_client_info_types(),
        'duration' : logic.all_durations(),
        'final' : deliverable.final,
        'dl' : deliverable,
        'review' : deliverable.review,
    })