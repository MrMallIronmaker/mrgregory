from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'paperwork/home.html')

def login_page(request):
    if request.method == "POST":
        # Auto login the user
        username = request.POST["username"]
        password = request.POST["password"]
        next_url = '/'
        if "next" in request.POST:
            next_url = request.POST["next"]
        a_u = authenticate(username=username, password=password)
        if a_u is not None:
            if a_u.is_active:
                login(request, a_u)
                return HttpResponseRedirect(next_url)
    else:
        # when you load the page to login, it's a GET variable.
        next_url = '/'
        if "next" in request.GET:
            next_url = request.GET["next"]

    return render(request, 'paperwork/login.html', {
        "next" : next_url
        })
