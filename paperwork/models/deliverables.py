""" Deliverables: The things you get done. """
from enum import Enum

from django.db import models

# pylint: disable=too-few-public-methods
# this is OK disabled because enums usually have few public methods.
class Duration(Enum):
    """Durations represent lengtsh of time before or after deadlines"""
    @staticmethod
    def pretty_print(index):
        """ the human-readable version of the durations."""
        if index == 1:
            return "calendar day(s)"
        elif index == 2:
            return "business day(s)"
        return "[unknown duration(s)]"

    def __str__(self):
        return self.pretty_print(self.value)
    def __unicode__(self):
        return self.__str__()

    calendar_day = 1
    business_day = 2
# pylint: enable=too-few-public-methods
DURATION_CHOICES = ((d.value, d.name) for d in Duration)

# deliverable models
class Deliverable(models.Model):
    """
    Deadlines all have a deliverable, and each deliverable has exactly one
    main deadline.
    """
    # all deliverable have a title, e.g, "mental
    # health assessment, annual review"
    title = models.CharField(max_length=200)
    # all deliverables have a final deadline
    final = models.OneToOneField('FinalDeadline', on_delete=models.CASCADE)
    review = models.OneToOneField(
        'ReviewDeadline',
        null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.__str__()

class Deadline(models.Model):
    """ Deadlines have a way to calculate a date."""
    # each deadline has a name.
    title = models.CharField(max_length=200)

    offset = models.IntegerField()
    duration = models.IntegerField(choices=DURATION_CHOICES)

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.__str__()

    # TODO: singularize [e.g, day not days] when offset = 1
    def english_offset(self):
        """ convert deadline information to human-readable"""
        if self.offset > 0:
            return str(self.offset) + " " + \
                Duration.pretty_print(self.duration) + " after"
        elif self.offset < 0:
            return str(-self.offset) + " " + \
                Duration.pretty_print(self.duration) + " before"
        return "the same " + Duration.pretty_print(self.duration) + " as"

    @property
    def deliverable(self):
        if hasattr(self, "stepdeadline"):
            return self.stepdeadline.deliverable
        elif hasattr(self, "finaldeadline"):
            return self.finaldeadline.deliverable
        elif hasattr(self, "reviewdeadline"):
            return self.reviewdeadline.deliverable
        else:
            raise TypeError("Deadline does not have a deliverable???")

    def abs_offset(self):
        return abs(self.offset)

    def is_before(self):
        return self.offset < 0

    def is_after(self):
        return self.offset > 0

class FinalDeadline(Deadline):
    """ the last deadline, where everything is due."""
    # a final deadline is relative to some type of Client Info
    relative_info_type = models.ForeignKey(
        'ClientInfoType',
        on_delete=models.CASCADE)
    # TODO: don't cascade, instead create an error.
    def __unicode__(self):
        return super.__str__()

class StepDeadline(Deadline):
    """ deadlines that refer to other deadlines """
    # each deadline is part of a deliverable
    deliverable = models.ForeignKey(
        Deliverable,
        on_delete=models.CASCADE,
        related_name="step_deadlines")
    # a step deadline is relative to some other deadline
    ancestor = models.ForeignKey(
        Deadline,
        on_delete=models.CASCADE,
        related_name="children")
    def __unicode__(self):
        return super.__str__()

class ReviewDeadline(Deadline):
    """ Deadline for the nth time around """
    relative_info_type = models.ForeignKey(
        'ClientInfoTypeSignature',
        on_delete=models.CASCADE)
    def __unicode__(self):
        return super.__str__()
