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
