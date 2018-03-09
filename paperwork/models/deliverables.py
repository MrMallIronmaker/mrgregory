from django.db import models
from enum import Enum

class Duration(Enum):
    @staticmethod
    def pretty_print(index):
        if index == 1:
            return "calendar day(s)"
        elif index == 2:
            return "business day(s)"
        else:
            return "[unknown duration(s)]"

    def __str__(self):
        return self.pretty_print(self.value)

    calendar_day = 1
    business_day = 2
DURATION_CHOICES = ((d.value, d.name) for d in Duration)

# deliverable models
class Deliverable(models.Model):
    # all deliverable have a title, e.g, "mental health assessment, annual review"
    title = models.CharField(max_length=200)
    # all deliverables have a final deadline
    final = models.OneToOneField('FinalDeadline', on_delete=models.CASCADE)
    review = models.OneToOneField('ReviewDeadline', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Deadline(models.Model):
    # each deadline has a name.
    title = models.CharField(max_length=200)

    offset = models.IntegerField()
    duration = models.IntegerField(choices=DURATION_CHOICES)

    def __str__(self):
        return self.title

    # TODO: singularize [e.g, day not days] when offset = 1
    def pretty_offset(self):
        if self.offset > 0:
            return str(self.offset) + " " + \
                Duration.pretty_print(self.duration) + " after"
        elif self.offset < 0:
            return str(-self.offset) + " " + \
                Duration.pretty_print(self.duration) + " before"
        else:
            return "the same " + Duration.pretty_print(self.duration) + " as"

class FinalDeadline(Deadline):
    # a final deadline is relative to some type of Client Info
    relative_info_type = models.ForeignKey('ClientInfoType', on_delete=models.CASCADE)
    # TODO: don't cascade, instead create an error.
    # TODO: what if the deadline is absolute?

class StepDeadline(Deadline):
    # each deadline is part of a deliverable
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE, related_name="step_deadlines")
    # a step deadline is relative to some other deadline
    ancestor = models.ForeignKey(Deadline, on_delete=models.CASCADE, related_name="children")

class ReviewDeadline(Deadline):
    relative_info_type = models.ForeignKey('ClientInfoTypeSignature', on_delete=models.CASCADE)