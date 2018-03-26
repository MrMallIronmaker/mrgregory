from django.test import LiveServerTestCase
from selenium import webdriver

class WebTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(WebTestCase, cls).setUpClass()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(WebTestCase, cls).tearDownClass()

    def test_sanity(self):
        self.browser.get(self.live_server_url)