# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Client information is stored as a cross between clients and info type.
class Client(models.Model):
    # every client has a name
    name = models.CharField(max_length=10)

class ClientInfoType(models.Model):
    # each information type has a name
    title = models.CharField(max_length=200) # e.g, "Last visit" or

class ClientInfo(models.Model):
    # each piece of information has a client it's referring to
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # and a type of information
    info_type = models.ForeignKey(ClientInfoType, on_delete=models.CASCADE)

class ClientInfoDate(ClientInfo):
    # sometimes that information has a date
    date = models.DateField()

# deliverable models
class Deliverable(models.Model):
    # all deliverable have a title, e.g, "mental health assessment, annual review"
    title = models.CharField(max_length=200)
    # all deliverables have a final deadline
    final = models.OneToOneField('FinalDeadline', on_delete=models.CASCADE)

class Deadline(models.Model):
    # all deadlines have a deliverable, but sometimes that's the reference of the
    # final table

    #TODO: fix this assumption?: each deadline has a time offset in days, we'll say
    offset = models.IntegerField()

class FinalDeadline(Deadline):
    # a final deadline is relative to some type of Client Info
    relative_info_type = models.ForeignKey(ClientInfoType, on_delete=models.CASCADE)
    # TODO: don't cascade, instead create an error.
    # TODO: what if the deadline is absolute?

class StepDeadline(Deadline):
    # each deadline is part of a deliverable
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE)
    # a step deadline is relative to some other deadline
    ancestor = models.ForeignKey(Deadline, on_delete=models.CASCADE, related_name="children")

# not yet
#class Contingencies(models.Model):

# for each client, for each deadline, there is a task.
#class Tasks(models.Model):
#    pass