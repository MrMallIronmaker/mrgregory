from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from paperwork import logic

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
def view_clients(request):
    """
    Display list of clients. Someday soon, add links to client info [editable]
    """
    # does the request have a post option?
    # if so, add it to the database.
    if "name" in request.POST:
        logic.create_client(request.POST)

    return render(request, 'paperwork/clients.html', {
        'client_info_type_list' : logic.all_client_info_types(),
        'client_list' : logic.all_clients(),
    })
