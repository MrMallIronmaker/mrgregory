from django.test import TestCase
import datetime

import logic
from models import ClientInfoType, Client, ClientInfo

cit_title = "initial appointment"

class IntegrationTestCase(TestCase):

    def create_cit(self):
        logic.create_client_info_type(cit_title)

    def test_create_cit(self):
        self.create_cit()
        cits = ClientInfoType.objects.filter(title=cit_title)
        self.assertTrue(len(cits) == 1)
        self.assertTrue(cits[0].title == cit_title)

    def test_create_client(self):
        start_date = datetime.date(2018, 3, 1)
        start_date_string = start_date.strftime("%Y-%m-%d")
        name = "JD"
        self.create_cit()
        logic.create_client({
            "name" : name,
            cit_title : start_date_string
            })
        clients = Client.objects.filter(name=name)
        self.assertTrue(len(clients) == 1)

        cit = ClientInfoType.objects.get(title=cit_title)
        info = ClientInfo.objects.get(client=clients[0], info_type=cit)
        self.assertTrue(hasattr(info, "clientinfodate"))
        self.assertTrue(info.clientinfodate.date == start_date)