"""
Models for the Tasks that are generated. 
Depends on Clients and Deliverables.
"""
from django.db import models

class TaskStatus(models.Model):
    """ Does little Jimmy need a Columbia Impairment Scale? """
    # each task needs a client
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    # and a deliverable
    deliverable = models.ForeignKey('Deliverable', on_delete=models.CASCADE)
    # and this says whether it's needed or not
    needed = models.BooleanField()

    def __str__(self):
        return "{0} {1} {2}".format(
        	   self.client,
        	   ["does not need", "needs"][int(self.needed)],
        	   self.deliverable)

    def __unicode__(self):
        return self.__str__()

class Task(models.Model):
    """ When do I need to get little Jimmy's MHA to my supervisor? """
    # refer to a test_status
    task_status = models.ForeignKey('TaskStatus', on_delete=models.CASCADE)
    # what deadline it refers to
    deadline = models.ForeignKey('Deadline', on_delete=models.CASCADE)
    # when it's due
    date = models.DateField()
    # whether it's done
    completed = models.BooleanField()

    def __str__(self):
        return "{0} for {1}'s {2} is due {3}{4}".format(
            self.deadline,
            self.task_status.client,
            self.task_status.deliverable,
            self.date,
            ["", " (completed)"][int(self.completed)])

    def __unicode__(self):
        return self.__str__()
