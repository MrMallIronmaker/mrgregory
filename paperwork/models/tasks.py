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