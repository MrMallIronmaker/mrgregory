from django.test import TestCase

class ClientsTestCase(TestCase):
    def test_sanity(self):
        self.assertEqual(1, 1)