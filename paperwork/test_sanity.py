from django.test import TestCase

class SanityTestCase(TestCase):
    def test_sanity(self):
        self.assertEqual(1, 1)