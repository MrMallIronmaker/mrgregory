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
        return "{client} {may_need} {deliverable}".format(
        	   client=self.client,
        	   may_need=["does not need", "needs"][int(self.needed)],
        	   deliverable=self.deliverable)

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
        fmt = "{deadline} for {client}'s {deliverable} is due {date}{completed}"
        return fmt.format(
            deadline=self.deadline,
            client=self.task_status.client,
            deliverable=self.task_status.deliverable,
            date=self.date,
            completed=["", " (completed)"][int(self.completed)])

    def __unicode__(self):
        return self.__str__()
