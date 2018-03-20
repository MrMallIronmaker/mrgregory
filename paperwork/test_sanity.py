"""A single sanity check case"""

from django.test import TestCase

class SanityTestCase(TestCase):
    """Class for the sanity check"""
    def test_sanity(self):
        """
        This test should always past if the testing environment is logical
        """
        self.assertEqual(1, 1)
