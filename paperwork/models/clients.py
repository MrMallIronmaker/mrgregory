""" This is who it's all about. Clients and their needs."""

from django.db import models

# Client information is stored as a cross between clients and info type.
class Client(models.Model):
    """who are you treating?"""
    # every client has a name
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

class ClientInfoType(models.Model):
    """ represents the kinds of information to keep track of"""
    # each information type has a name
    title = models.CharField(max_length=200) # e.g, "Last visit" or

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.__str__()

class ClientInfoTypeSignature(ClientInfoType):
    """ Automatically generated by each deliverable"""
    # also include deliverable
    deliverable = models.OneToOneField('Deliverable')

    def __unicode__(self):
        return self.__str__()

class ClientInfo(models.Model):
    """ connects clients and info types. Needs a subclass to make sense"""
    # each piece of information has a client it's referring to
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # and a type of information
    info_type = models.ForeignKey(ClientInfoType, on_delete=models.CASCADE)

    def __str__(self):
        return "{client}'s {info_type}".format(
            client=self.client, info_type=self.info_type)
    def __unicode__(self):
        return self.__str__()

    def pretty_print(self):
        if hasattr(self, "clientinfodate"):
            return self.clientinfodate.pretty_print()
        else:
            raise TypeError("ClientInfo must have a subclass.")

class ClientInfoDate(ClientInfo):
    """ sometimes that information has a date """
    date = models.DateField(null=True) # the date may not have happened yet

    def __str__(self):
        if self.date:
            return "{client_info} was {date}".format(
                client_info=self.clientinfo_ptr, date=self.date)
        return "{client_info} has not occurred".format(
            client_info=self.clientinfo_ptr)

    def __unicode__(self):
        return self.__str__()

    def pretty_print(self):
        if self.date:
            return self.date.strftime("%Y-%m-%d")

        return ""
