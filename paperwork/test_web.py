""" Tests for the web-particular things. Like clicking on buttons. """
import unittest, time, re
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

class WebTestCase(LiveServerTestCase):
    """ Functional tests for the way Jordan may use the website"""
    @classmethod
    def setUpClass(cls):
        """ Create the webdriver """
        super(WebTestCase, cls).setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        """
        Quit the webdriver so firefox windows
        aren't littering my desktop
        """
        cls.driver.quit()
        super(WebTestCase, cls).tearDownClass()

    def setUp(self):
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    def test_sanity(self):
        """ a simple test case """
        self.driver.get(self.live_server_url)
    
    def test_login(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.find_element_by_link_text("deliverables").click()
        self.assertEqual(driver.current_url, self.live_server_url + "/login/?next=/deliverables/")
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("test")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("selenium")
        driver.find_element_by_xpath("//input[@value='Login']").click()
        self.assertEqual(self.live_server_url + "/deliverables/", driver.current_url)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
