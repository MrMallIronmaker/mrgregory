from django.test import TestCase
import datetime

import logic
from models import ClientInfoType, Client, ClientInfo, Duration, Deliverable

# config info
cit_title = "initial appointment"

client_name = "JD"
start_date = datetime.date(2018, 3, 1)

class IntegrationTestCase(TestCase):

    def create_cit(self):
        logic.create_client_info_type(cit_title)

    def test_create_cit(self):
        self.create_cit()
        cits = ClientInfoType.objects.filter(title=cit_title)
        self.assertTrue(len(cits) == 1)
        self.assertTrue(cits[0].title == cit_title)

    def create_client(self):
        start_date_string = start_date.strftime("%Y-%m-%d")
        self.create_cit()
        logic.create_client({
            "name" : client_name,
            cit_title : start_date_string
            })

    def test_create_client(self):
        self.create_client()
        clients = Client.objects.filter(name=client_name)
        self.assertTrue(len(clients) == 1)
        cit = ClientInfoType.objects.get(title=cit_title)
        info = ClientInfo.objects.get(client=clients[0], info_type=cit)
        self.assertTrue(hasattr(info, "clientinfodate"))
        self.assertTrue(info.clientinfodate.date == start_date)

    def test_create_deliverable(self):
        self.create_cit()
        cit = ClientInfoType.objects.get(title=cit_title)
        mha_title = "mental health assessment"
        logic.create_deliverable({
            "anchor" : cit.id,
            "number" : 30,
            "duration" : Duration.calendar_day.value,
            "relation" : "after",
            "title" : mha_title,
            "review_offset" : 90,
            "review_duration" : Duration.calendar_day.value,
            "review" : 1
            })
        # are there results?
        deliverables = Deliverable.objects.filter(title=mha_title)
        self.assertTrue(len(deliverables) == 1)
        self.assertTrue(deliverables[0].title == mha_title)