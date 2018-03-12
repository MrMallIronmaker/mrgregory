from django.test import TestCase

class ClientsTestCase(TestCase):
    def test_sanity(self):
        return self.assertEqual(1, 2)