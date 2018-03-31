""" Tests for the web-particular things. Like clicking on buttons. """
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium.webdriver.support.ui import Select
from selenium import webdriver

from paperwork.test_integration import create_cit

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
        self.driver.implicitly_wait(5)
        self.verification_errors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual([], self.verification_errors)

    def test_sanity(self):
        """ a simple test case """
        self.driver.get(self.live_server_url)

    def login(self):
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

    def test_login(self):
        self.login()

        # this should be a success!
        self.assertEqual(self.live_server_url + "/deliverables/",
                         self.driver.current_url)

    def test_massive_test(self):
        # begin by logging in
        self.login()
        create_cit()

        # now do more.
        driver = self.driver
        driver.get(self.live_server_url)
        driver.find_element_by_link_text("clients").click()
        driver.find_element_by_link_text("deliverables").click()
        driver.find_element_by_link_text("New Deliverable").click()
        title = driver.find_element_by_name("title")
        title.click()
        title.clear()
        title.send_keys("Mental Health Assessment")
        driver.find_element_by_name("number").clear()
        driver.find_element_by_name("number").send_keys("30")
        relation = driver.find_element_by_name("relation")
        Select(relation).select_by_visible_text("after")
        driver.find_element_by_name("review_offset").clear()
        driver.find_element_by_name("review_offset").send_keys("360")
        driver.find_element_by_xpath("//input[@value='submit']").click()
        driver.find_element_by_xpath("//body").click()
        driver.find_element_by_xpath("//body").click()
        
        nd_title = driver.find_element_by_name("nd-title")
        nd_title.clear()
        nd_title.send_keys("submit to my supervisor")
        driver.find_element_by_name("nd-number").clear()
        driver.find_element_by_name("nd-number").send_keys("3")
        nd_duration = driver.find_element_by_name("nd-duration")
        Select(nd_duration).select_by_visible_text("business day(s)")
        driver.find_element_by_xpath("//input[@value='submit']").click()

        nd_title = driver.find_element_by_name("nd-title")
        nd_title.click()
        nd_title.clear()
        nd_title.send_keys("collect all collaterals")
        driver.find_element_by_name("nd-number").clear()
        driver.find_element_by_name("nd-number").send_keys("7")
        driver.find_element_by_xpath("//input[@value='submit']").click()

        nd_title = driver.find_element_by_name("nd-title")
        nd_title.click()
        nd_title.clear()
        nd_title.send_keys("reach out to collaterals")
        driver.find_element_by_name("nd-number").clear()
        driver.find_element_by_name("nd-number").send_keys("14")
        nd_anchor = driver.find_element_by_name("nd-anchor")
        Select(nd_anchor).select_by_visible_text("collect all collaterals")
        driver.find_element_by_xpath("//input[@value='submit']").click()

        offset_textbox = driver.find_element_by_xpath(
            '//li[3]/form/input[@type="number"]')
        offset_textbox.click()
        offset_textbox.clear()
        offset_textbox.send_keys("7")
        driver.find_element_by_xpath(
            "(//input[@value='save edits'])[3]"
            ).click()
        driver.find_element_by_link_text("Edit").click()
        driver.find_element_by_name("review_offset").click()
        driver.find_element_by_name("review_offset").clear()
        driver.find_element_by_name("review_offset").send_keys("365")
        driver.find_element_by_xpath("//input[@value='submit']").click()
        #TODO: some xpath checking here
        """
         self.assertEqual("Mental Health Assessment This deliverable is due 30
         calendar day(s) after the client's initial appointment.\n The reviews
         are due 365 calendar day(s) after the most recent signature.\n \n \n
         Edit \n \n I know about these other deadlines:\n calendar day(s)
         business day(s) before after you submit to my supervisor collect all
         collaterals reach out to collaterals Mental Health Assessment calendar
         day(s) business day(s) before after you submit to my supervisor collect
         all collaterals reach out to collaterals Mental Health Assessment
         calendar day(s) business day(s) before after you submit to my
         supervisor collect all collaterals reach out to collaterals Mental
         Health Assessment \n I want to calendar day(s) business day(s) before
         after I submit to my supervisor collect all collaterals reach out to
         collaterals Mental Health Assessment \n \n When you're finished adding
         deadlines, you can return to the deliverables. \n home | clients |
         deliverables | who gets what | tasks",
         driver.find_element_by_xpath("//body").text)
        """
        driver.find_element_by_link_text("deliverables").click()
        driver.find_element_by_link_text("New Deliverable").click()
        driver.find_element_by_name("title").click()
        driver.find_element_by_name("title").clear()
        driver.find_element_by_name("title").send_keys("something else")
        driver.find_element_by_name("number").clear()
        driver.find_element_by_name("number").send_keys("90")

        relation = driver.find_element_by_name("relation")
        Select(relation).select_by_visible_text("after")
        review = driver.find_element_by_id("review")
        Select(review).select_by_visible_text("does not need")
        driver.find_element_by_xpath("//input[@value='submit']").click()
        driver.find_element_by_link_text("deliverables").click()
        driver.find_element_by_link_text("clients").click()

        driver.find_element_by_name("name").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("SW")
        initial_appointment = driver.find_element_by_name("initial appointment")
        initial_appointment.clear()
        initial_appointment.send_keys("2018-03-10")
        driver.find_element_by_xpath("//input[@value='submit']").click()

        driver.find_element_by_name("name").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("JD")
        initial_appointment = driver.find_element_by_name("initial appointment")
        initial_appointment.clear()
        initial_appointment.send_keys("2018-02-01")
        signature = driver.find_element_by_name(
            "signature of Mental Health Assessment")
        signature.clear()
        signature.send_keys("2018-02-20")
        driver.find_element_by_xpath("//input[@value='submit']").click()
        driver.find_element_by_link_text("JD").click()

        signature = driver.find_element_by_name(
            "signature of Mental Health Assessment")
        signature.click()
        signature.clear()
        signature.send_keys("2018-02-22")
        driver.find_element_by_xpath("//input[@value='update']").click()
        driver.find_element_by_link_text("Return to clients listing.").click()
        driver.find_element_by_link_text(
            "specify what clients need which deliverables.").click()

        driver.find_element_by_xpath("//tbody/tr[2]/td[2]/input").click()
        driver.find_element_by_xpath("//tbody/tr[2]/td[3]/input").click()
        driver.find_element_by_xpath("//tbody/tr[3]/td[3]/input").click()
        driver.find_element_by_xpath("//input[@value='Submit']").click()

        # TODO: assert something about the database status here

        def td_checkbox_checked_attr(row, col):
            format_string = "//tbody/tr[{t_row}]/td[{t_col}]/input"
            xpath = format_string.format(t_row=row+2, t_col=col+2)
            return driver.find_element_by_xpath(xpath).get_attribute("checked")

        self.assertEqual("true", td_checkbox_checked_attr(0, 0))
        self.assertEqual("true", td_checkbox_checked_attr(0, 1))
        self.assertEqual("true", td_checkbox_checked_attr(1, 1))
        self.assertEqual(None, td_checkbox_checked_attr(1, 0))

        driver.find_element_by_link_text("here").click()
        self.assertEqual(
            "complete reach out to collaterals for SW's Mental Health "
            "Assessment is due 2018-03-20",
            driver.find_element_by_xpath("//li").text)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Swap between done and to do.").click()
        self.assertEqual(
            "un-complete reach out to collaterals for SW's Mental Health "
            "Assessment is due 2018-03-20 (completed)",
            driver.find_element_by_xpath("//li").text)
        driver.find_element_by_xpath("//i[2]").click()

        def get_text_of_h4_at_index(index):
            xpath = "//h4[{index}]".format(index=index)
            return driver.find_element_by_xpath(xpath).text

        self.assertEqual("March 27, 2018", get_text_of_h4_at_index(1))
        self.assertEqual("April 3, 2018", get_text_of_h4_at_index(2))
        self.assertEqual("April 9, 2018", get_text_of_h4_at_index(3))
        self.assertEqual("May 2, 2018", get_text_of_h4_at_index(4))
        self.assertEqual("Feb. 4, 2019", get_text_of_h4_at_index(5))
        self.assertEqual("Feb. 11, 2019", get_text_of_h4_at_index(6))
        self.assertEqual("Feb. 18, 2019", get_text_of_h4_at_index(7))
        self.assertEqual("Feb. 22, 2019", get_text_of_h4_at_index(8))
        driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
        self.assertEqual("March 11, 2019", get_text_of_h4_at_index(6))
        self.assertEqual("March 18, 2019", get_text_of_h4_at_index(7))
        self.assertEqual("March 25, 2019", get_text_of_h4_at_index(8))
        self.assertEqual("March 29, 2019", get_text_of_h4_at_index(9))
