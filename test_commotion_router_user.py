"""Sample automated test suite for commotion router's unprivileged functions.
    Most of these are an inefficient use of selenium, 
    but are included as examples.
"""

# pylint complains about unittest's method names
#method-rgx=(([a-z_][a-z0-9_]{2,30})| \
#    (setUp)|(setUpClass)|(tearDown)|(tearDownClass))$

# To do:
# Write Commotion-Router UI map for Selenium
# (See also Page Object Design Pattern)
# Write input fuzzers
# Write logging functions

import unittest
import commotiontestobjects.commotionrouterobjects.routerobjects as cro
#from commotiontestobjects.util import error
import commotiontestobjects.browserobjects as sel
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logging.basicConfig(filename='logs/test_commotion_router_ui.log',
                    level=logging.INFO)
logging.warning("Specify path to log directory")
logging.warning("This test suite needs a UI map!")


class CRInputTestCase(unittest.TestCase):
    """Setting defaults for live commotion router testing"""
    browser = "firefox"
    profile = "default"

    @classmethod
    def setUpClass(cls):
        """Get information about net interfaces and target commotion node"""
        cls.netinfo = {}
        cls.netinfo = cro.get_net_info(cls.netinfo)

    @classmethod
    def load_browser(cls, browser, profile):
        """
        Pass request to browser generation function with desired browser
        and profile type
        """
        browser = sel.request_browser(browser, profile)
        return browser

    @classmethod
    def tearDownClass(cls):
        cls.netinfo = {}
        cls.profile = None
        cls.browser = None
        logging.info("CRInputTestCase destroyed")


class TestCRUserFunctions(CRInputTestCase):
    """Unittest child class for unprivileged functions"""
    def setUp(self):
        """Set up browser"""
        self.browser = self.load_browser(self.browser, self.profile)

    @unittest.skipIf(1 == 1,
                     "Skip if wlan0 provides commotion ip and eth0 is in use")
    def test_thisnode(self):
        """Test thisnode dns resolution"""
        # SKIP THIS TEST if wlan0 provides commotion ip and eth0 is in use
        __sb = self.browser
        __sb.get('https://thisnode')
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(__sb.find_element_by_id("device"))

    def test_ip_address(self):
        """Test ip-only connection"""
        __sb = self.browser
        __sb.get('https://' + self.netinfo.commotion_node_ip)
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(__sb.find_element_by_id("device"))

    def tearDown(self):
        self.browser.quit()
        logging.info("Browser instance destroyed")


class TestCRAdminFunctions(CRInputTestCase):
    """Test admin functions. Note browser profile change"""

    profile = "firefox_admin"

    def setUp(self):
        """Set up browser to allow access to admin functions"""
        self.browser = self.load_browser(self.browser, self.profile)

    def test_require_admin_password(self):
        """
        Make sure a password is required for admin pages.
        Use admin profile to avoid DOM-less self-signed cert error.
        """
        __sb = self.browser
        url = 'https://' + self.netinfo.commotion_node_ip \
            + '/cgi-bin/luci/admin'
        __sb.get(url)
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        self.assertTrue(__sb.find_element_by_class_name("cbi-input-user"))

    def test_log_in_fail(self):
        """Incorrect password should return error"""
        __sb = self.browser
        url = 'https://' + self.netinfo.commotion_node_ip \
            + '/cgi-bin/luci/admin'
        __sb.get(url)
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        pw_field = __sb.find_element_by_id("focus_password")
        pw_field.send_keys("BADPASS\n")
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error")))
        self.assertTrue(__sb.find_element_by_class_name("error"))

    def test_fuzz_admin_password_field(self):
        """Try to break password function using garbage input"""
        # This should eventually replace test_log_in_fail
        __sb = self.browser
        url = 'https://' + self.netinfo.commotion_node_ip \
            + '/cgi-bin/luci/admin'
        __sb.get(url)
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        # fuzz = gen_fuzz(params)
        # for garbage in fuzz:
        #       pw_field = __sb.find_element_by_id("focus_password")
        #       pw_field.send_keys(garbage)
        #       WebDriverWait(__sb, 10).until(
        #           EC.presence_of_element_located((By.CLASS_NAME, "error")))
        #       seleniumVerifyTrue(__sb.find_element_by_class_name("error"))
        # assertTrue(noSeleniumVerifyFailures)

    def test_log_in_pass(self):
        """Correct password should allow access to privileged functions"""
        __sb = self.browser
        url = 'https://' + self.netinfo.commotion_node_ip \
            + '/cgi-bin/luci/admin'
        __sb.get(url)
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        __sb.find_element_by_id("focus_password").send_keys('asdf')
        # Should actually check for div.error
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.ID, "xhr_poll_status")))
        self.assertTrue(__sb.find_element_by_id("xhr_poll_status"))

    def tearDown(self):
        """Clean up test instance"""
        self.browser.quit()
        logging.info("Browser instance destroyed")

if __name__ == "__main__":
    # This is probably wrong
    def suite():
        """Gather all tests from this module into a test suite."""
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(CRInputTestCase))
        test_suite.addTest(unittest.makeSuite(TestCRUserFunctions))
        test_suite.addTest(unittest.makeSuite(TestCRAdminFunctions))
        return test_suite
    # Fix logging
    # https://stackoverflow.com/questions/3347019/\
    #    how-can-one-use-the-logging-module-in-python-with-the-unittest-module
    browser_suite = suite()
    runner = unittest.TextTestRunner()
    runner.run(browser_suite)
