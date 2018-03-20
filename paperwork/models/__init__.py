"""
Module for all the paperwork models. They are split into three main groups,
clients, deliverables, and tasks.
"""

from paperwork.models.clients import Client, ClientInfoType, ClientInfo, \
    ClientInfoDate, ClientInfoTypeSignature
from paperwork.models.deliverables import Deliverable, Deadline, \
    FinalDeadline, StepDeadline, Duration, ReviewDeadline
from paperwork.models.tasks import TaskStatus, Task
