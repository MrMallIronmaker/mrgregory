# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Client, ClientInfoType, ClientInfo, Deadline, \
    Deliverable, FinalDeadline, StepDeadline

# Register your models here.

admin.site.register(ClientInfoType)
admin.site.register(Client)
admin.site.register(ClientInfo)
admin.site.register(Deadline)
admin.site.register(Deliverable)
admin.site.register(FinalDeadline)
admin.site.register(StepDeadline)