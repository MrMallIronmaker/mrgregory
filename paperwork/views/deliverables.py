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

def new_deadline(request, deliverable_id):
    # setup
    deliverable = logic.get_deliverable_by_id(deliverable_id)

    # if valid POST:
    deadline_reqs = ["title", "anchor", "number", "duration", "relation"]
    if all([i in request.POST for i in deadline_reqs]):
        logic.create_deadline(deliverable, request.POST)

    return HttpResponseRedirect(reverse('paperwork:deliverable',
                        args=(deliverable.id,)))
