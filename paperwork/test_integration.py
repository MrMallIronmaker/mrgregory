from django.test import TestCase
import datetime

import logic
from models import deliverables, clients, tasks

# config info
cit_title = "initial appointment"

client_name = "JD"
start_date = datetime.date(2018, 3, 5)

other_client_name = "QZ"
other_start_date = datetime.date(2018, 3, 19)

mha_title = "mental health assessment"
s2s_title = "submit to supervisor"
deliverable_2_title = "second deliverable"

class IntegrationTestCase(TestCase):

    def create_cit(self):
        if len(clients.ClientInfoType.objects.filter(title=cit_title)) != 0:
            return
        logic.create_client_info_type(cit_title)

    def get_test_cit(self):
        return clients.ClientInfoType.objects.get(title=cit_title)

    def test_create_cit(self):
        self.create_cit()
        cits = clients.ClientInfoType.objects.filter(title=cit_title)
        self.assertEqual(len(cits), 1)
        self.assertEqual(cits[0].title, cit_title)

    def create_client(self):
        if len(clients.Client.objects.filter(name=client_name)) != 0:
            return
        start_date_string = start_date.strftime("%Y-%m-%d")
        self.create_cit()
        logic.create_client({
            "name" : client_name,
            cit_title : start_date_string
            })

    def get_test_client(self):
        return clients.Client.objects.get(name=client_name)

    def test_create_client(self):
        self.create_client()
        client_list = clients.Client.objects.filter(name=client_name)
        self.assertEqual(len(client_list), 1)
        cit = clients.ClientInfoType.objects.get(title=cit_title)
        info = clients.ClientInfo.objects.get(client=client_list[0], info_type=cit)
        self.assertTrue(hasattr(info, "clientinfodate"))
        self.assertEqual(info.clientinfodate.date, start_date)

    def create_deliverable(self):
        if len(deliverables.Deliverable.objects.filter(title=mha_title)) != 0:
            return
        self.create_cit()
        cit = self.get_test_cit()
        logic.create_deliverable({
            "anchor" : cit.id,
            "number" : 30,
            "duration" : deliverables.Duration.calendar_day.value,
            "relation" : "after",
            "title" : mha_title,
            "review_offset" : 90,
            "review_duration" : deliverables.Duration.calendar_day.value,
            "review" : 1
            })

    def get_test_deliverable(self):
        return deliverables.Deliverable.objects.get(title=mha_title)

    def test_create_deliverable(self):
        self.create_deliverable()
        # are there results?
        deliverables_filter = deliverables.Deliverable.objects.filter(title=mha_title)
        self.assertEqual(len(deliverables_filter), 1)
        self.assertEqual(deliverables_filter[0].title, mha_title)

    def create_deadline(self):
        self.create_deliverable()
        deliverable = self.get_test_deliverable()
        logic.create_deadline(deliverable, {
            "anchor" : deliverable.final.deadline_ptr.id,
            "number" : 3,
            "duration" : deliverables.Duration.business_day.value,
            "relation" : "before",
            "title" : s2s_title
            })

    def get_test_deadline(self):
        return deliverables.Deadline.objects.get(title=s2s_title)

    def test_create_deadline(self):
        self.create_deadline()

        other_deadlines = deliverables.Deadline.objects.filter(title=s2s_title)
        self.assertEqual(len(other_deadlines), 1)
        self.assertEqual(other_deadlines[0].offset, -3)

    def set_task_status(self):
        self.create_deliverable()
        self.create_client()
        client = self.get_test_client()
        deliverable = self.get_test_deliverable()
        logic.update_task_statuses({
            "c{0}-d{1}".format(client.id, deliverable.id) : "on" 
            })

    def test_set_task_status(self):
        self.set_task_status()
        client = self.get_test_client()
        deliverable = self.get_test_deliverable()
        task_statuses = tasks.TaskStatus.objects.filter(
            client=client,
            deliverable=deliverable)
        self.assertEqual(len(task_statuses), 1)
        self.assertTrue(task_statuses[0].needed)

    def get_test_task_status(self):
        client = self.get_test_client()
        deliverable = self.get_test_deliverable()
        return tasks.TaskStatus.objects.get(client=client, deliverable=deliverable)

    def get_other_test_task_status(self):
        # TODO: refactor this?
        client = self.get_test_client()
        other_deliverable = self.get_other_test_deliverable()
        return tasks.TaskStatus.objects.get(client=client, deliverable=other_deliverable)

    def assert_date_of_test_task(self):
        deliverable = self.get_test_deliverable()
        task_status = self.get_test_task_status()
        task_list = tasks.Task.objects.filter(
            task_status=task_status, 
            deadline=deliverable.final.deadline_ptr)
        self.assertEqual(len(task_list), 1)
        # 30 days ahead
        self.assertEqual(task_list[0].date, datetime.date(2018, 4, 4))

    def assert_date_of_test_deadline_task(self):
        deadline = self.get_test_deadline()
        task_status = self.get_test_task_status()
        task_list = tasks.Task.objects.filter(
            task_status=task_status, 
            deadline=deadline)
        self.assertEqual(len(task_list), 1)
        # 30 days ahead minus 3 business days
        self.assertEqual(task_list[0].date, datetime.date(2018, 3, 29))

    def test_create_tasks(self):
        # setup
        self.set_task_status()
        logic.create_tasks()

        # analyze
        self.assert_date_of_test_task()

    def test_multiple_tasks(self):
        self.create_deadline()
        self.set_task_status()
        logic.create_tasks()

        self.assert_date_of_test_task()
        self.assert_date_of_test_deadline_task()

    def create_multiple_deliverables(self):
        # make deliverables
        self.create_deliverable()
        cit = self.get_test_cit()
        
        logic.create_deliverable({
            "anchor" : cit.id,
            "number" : 90,
            "duration" : deliverables.Duration.calendar_day.value,
            "relation" : "after",
            "title" : deliverable_2_title,
            "review_offset" : 90,
            "review_duration" : deliverables.Duration.calendar_day.value,
            "review" : 1
            })

    def get_other_test_deliverable(self):
        return deliverables.Deliverable.objects.get(title=deliverable_2_title)

    def test_create_multiple_deliverables(self):
        self.create_multiple_deliverables()

        # assert the deliverables exist
        deliverable_2_list = deliverables.Deliverable.objects.filter(
            title=deliverable_2_title)
        self.assertEqual(len(deliverable_2_list), 1)
        self.assertEqual(deliverable_2_list[0].title, deliverable_2_title)

    def assert_date_of_other_test_task(self):
        other_deliverable = self.get_other_test_deliverable()
        task_status = self.get_other_test_task_status()
        task_list = tasks.Task.objects.filter(
            task_status=task_status, 
            deadline=other_deliverable.final.deadline_ptr)
        self.assertEqual(len(task_list), 1)
        # 90 days ahead
        self.assertEqual(task_list[0].date, datetime.date(2018, 6, 3))

    def get_other_test_client(self):
        return clients.Client.objects.get(name=other_client_name)

    def assert_date_of_other_client_test_task(self):
        other_client = self.get_other_test_client()
        deliverable = self.get_test_deliverable()
        task_status = tasks.TaskStatus.objects.get(
            client=other_client, deliverable=deliverable)
        
        task_list = tasks.Task.objects.filter(
            task_status=task_status, 
            deadline=deliverable.final.deadline_ptr)
        self.assertEqual(len(task_list), 1)
        # 30 days ahead
        self.assertEqual(task_list[0].date, datetime.date(2018, 4, 18))

    def test_tasks_from_multiple_deliverables(self):
        # create multiple deliverables
        self.create_multiple_deliverables()

        # set task statuses
        self.set_task_status()
        client = self.get_test_client()
        deliverable = self.get_test_deliverable()
        other_deliverable = self.get_other_test_deliverable()
        logic.update_task_statuses({
            "c{0}-d{1}".format(client.id, deliverable.id) : "on",
            "c{0}-d{1}".format(client.id, other_deliverable.id) : "on",
            })

        # make tasks
        logic.create_tasks()
        self.assert_date_of_test_task()
        self.assert_date_of_other_test_task()

    def create_multiple_clients(self):
        self.create_client()
        other_start_date_string = other_start_date.strftime("%Y-%m-%d")
        logic.create_client({
            "name" : other_client_name,
            cit_title : other_start_date_string
            })

    def test_create_multiple_clients(self):
        # setup
        self.create_multiple_clients()

        # TODO: abstract away, don't copy and paste
        client_list = clients.Client.objects.filter(name=other_client_name)
        self.assertEqual(len(client_list), 1)
        cit = clients.ClientInfoType.objects.get(title=cit_title)
        info = clients.ClientInfo.objects.get(client=client_list[0], info_type=cit)
        self.assertTrue(hasattr(info, "clientinfodate"))
        self.assertEqual(info.clientinfodate.date, other_start_date)

    def test_create_tasks_for_multiple_clients(self):
        # setup
        self.create_multiple_clients()

        # set task statuses
        self.set_task_status()
        client = self.get_test_client()
        deliverable = self.get_test_deliverable()
        other_client = self.get_other_test_client()
        logic.update_task_statuses({
            "c{0}-d{1}".format(client.id, deliverable.id) : "on",
            "c{0}-d{1}".format(other_client.id, deliverable.id) : "on",
            })

        logic.create_tasks()

        self.assert_date_of_test_task()
        self.assert_date_of_other_client_test_task()

