""" Tests for the web-particular things. Like clicking on buttons. """
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver

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
        self.verification_errors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual([], self.verification_errors)

    def test_sanity(self):
        """ a simple test case """
        self.driver.get(self.live_server_url)

    def test_login(self):
        driver = self.driver
        # visit the website
        driver.get(self.live_server_url)

        # ok, now that we know we're good, we can create the user.
        user = User.objects.create_user(
            username='test',
            email='test@testingfakeemail.com',
            password='selenium')
        user.save()

        # pretend the user wants to visit some page
        driver.find_element_by_link_text("deliverables").click()

        # oh no! redirected.
        self.assertEqual(
            driver.current_url,
            self.live_server_url + "/login/?next=/deliverables/")

        # so they login.
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("test")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("selenium")
        driver.find_element_by_xpath("//input[@value='Login']").click()

        # this should be a success!
        self.assertEqual(self.live_server_url + "/deliverables/",
                         driver.current_url)
