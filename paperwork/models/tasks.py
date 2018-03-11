from django.db import models

class TaskStatus(models.Model):
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

class Task(models.Model):
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
