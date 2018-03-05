from django.db import models

# Client information is stored as a cross between clients and info type.
class Client(models.Model):
    # every client has a name
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class ClientInfoType(models.Model):
    # each information type has a name
    title = models.CharField(max_length=200) # e.g, "Last visit" or

    def __str__(self):
        return self.title

class ClientInfo(models.Model):
    # each piece of information has a client it's referring to
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # and a type of information
    info_type = models.ForeignKey(ClientInfoType, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}'s {1}".format(self.client, self.info_type)

class ClientInfoDate(ClientInfo):
    # sometimes that information has a date
    date = models.DateField()

    def __str__(self):
        print dir(self)
        return "{0} was {1}".format(self.clientinfo_ptr, self.date)