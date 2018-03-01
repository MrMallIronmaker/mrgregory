# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.dateparse import parse_date
from django.urls import reverse

from .models import ClientInfoType, Client, ClientInfoDate, Deliverable, \
    Deadline, FinalDeadline, StepDeadline

from datetime import timedelta

# Create your views here.

def index(request):
    return render(request, 'paperwork/index.html')

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

def deliverables(request):

	return render(request, 'paperwork/deliverables.html', {
		'deliverable_list' : Deliverable.objects.all()
	})

def new_deliverable(request):
	# if there's a POST, process it and redirect.
	if all([i in request.POST for i in ["title", "anchor", "number", "deadline_title"]]):
		cit = ClientInfoType.objects.get(id=request.POST["anchor"])
		fd = FinalDeadline(
			relative_info_type=cit, 
			offset=request.POST["number"],
			title=request.POST["deadline_title"]
		)
		fd.save()
		deliverable = Deliverable(title=request.POST["title"], final=fd)
		deliverable.save()
		return HttpResponseRedirect(reverse('paperwork:deliverable', args=(deliverable.id,)))

	# if there's no POST, then just go ahead and display the page.
	return render(request, 'paperwork/new_deliverable.html', {
		'client_info_type_list' : ClientInfoType.objects.all(),
	})

def view_deliverable(request, deliverable_id):
	# setup
	deliverable = Deliverable.objects.get(id=deliverable_id)
	step_deadlines = [i for i in deliverable.step_deadlines.all()]
	deadlines = [i for i in step_deadlines] + [deliverable.final]

	# if valid POST:
	if all([i in request.POST for i in ["title", "anchor", "number"]]):
		step_deadline = StepDeadline(
			deliverable=deliverable, 
			ancestor=Deadline.objects.get(id=request.POST["anchor"]), 
			offset=request.POST["number"], 
			title=request.POST["title"])
		step_deadline.save()
		deadlines += [step_deadline]
		step_deadlines += [step_deadline]

	return render(request, 'paperwork/deliverable.html', {
		"dl" : deliverable,
		"step_deadlines" : step_deadlines,
		"deadlines" : deadlines,
	})

def tasks(request):
	# hack it out, mang.
	task_deadlines = {}
	task_strings = []
	tasks = []

	# first begin with the final deadlines, and work backwards
	for client in Client.objects.all():
		for fd in FinalDeadline.objects.all():
			# you ready? here goes.
			# get the info type entry
			cit = fd.relative_info_type
			# get the info entry date
			base_date = ClientInfoDate.objects.get(client=client, info_type=cit).date
			# calculate the offset from the date
			date = base_date + timedelta(fd.offset)
			task_deadlines[(client, fd)] = date
			task_strings.append("{0} for {1} due by {2}".format(
				fd.deliverable.title,
				client.name,
				date
			))
			tasks += [(client, i, fd) for i in fd.children.all()]

	while tasks:
		# you got this
		client, sd, fd = tasks.pop(0)
		# so the previous thing has a date of what?
		prev_date = task_deadlines[(client, sd.ancestor)]
		date = prev_date + timedelta(sd.offset)
		task_deadlines[(client, sd)] = date
		task_strings.append("{0} as part of {3} for {1} is due by {2}".format(
			sd.title,
			client.name,
			date,
			fd.deliverable.title
		))
		tasks += [(client, i, fd) for i in sd.children.all()]

	return render(request, 'paperwork/tasks.html', {
		"tasks" : task_strings
	})