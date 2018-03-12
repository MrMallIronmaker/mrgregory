from django.test import TestCase

class ClientsTestCase(TestCase):
    def sanity(self):
        return self.assertEqual(1, 2)