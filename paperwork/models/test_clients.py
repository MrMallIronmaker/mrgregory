"""
Unit tests for the clients model.
"""

from django.test import TestCase
from paperwork.models.clients import Client, ClientInfoType, ClientInfoDate

class ClientsTestCase(TestCase):
    """ unit tests for the clients model, class"""
    def test_nullability(self):
        """ it should be nullable because some dates haven't occured"""
        client = Client(name="JD")
        client.save()
        client_info_type = ClientInfoType(title="Fake Date")
        client_info_type.save()
        client_info_date = ClientInfoDate(
            client=client,
            info_type=client_info_type,
            date=None)
        # I know there's an exception thrown if the field is null and shouldn't
        # be, but I don't know which one, and I don't want to muck up the
        # database to find out.
        client_info_date.save()
        self.assertIsNone(client_info_date.date)
