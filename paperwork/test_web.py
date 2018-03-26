""" Tests for the web-particular things. Like clicking on buttons. """

from django.test import LiveServerTestCase
from selenium import webdriver

class WebTestCase(LiveServerTestCase):
    """ Functional tests for the way Jordan may use the website"""
    @classmethod
    def setUpClass(cls):
        """ Create the webdriver """
        super(WebTestCase, cls).setUpClass()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        """
        Quit the webdriver so firefox windows
        aren't littering my desktop
        """
        cls.browser.quit()
        super(WebTestCase, cls).tearDownClass()

    def test_sanity(self):
        """ a simple test case """
        self.browser.get(self.live_server_url)
