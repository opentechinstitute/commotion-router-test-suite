"""Sample automated test suite for Commotion Router"""
# To do:
# Write Commotion-Router UI map for Selenium
# (See also Page Object Design Pattern)
# Write input fuzzers
# Write admin module
# Write logging functions

import unittest
import netifaces as ni
import sys
import logging
import re
from selenium import webdriver
#from selenium.webdriver.firefox import firefox_profile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logging.basicConfig(filename='logs/test_commotion_router_ui.log',
                    level=logging.INFO)
logging.warning("Specify path to log directory")
logging.warning("This test suite needs a UI map!")

def error(message):
    """Simple error reporting"""
    logging.error(message)
    sys.stderr.write("ERROR: %s\n" % message)
    sys.exit(1)


class CRInputTestCase(unittest.TestCase):
    """Setting defaults for live commotion router testing"""

    @classmethod
    def setUpClass(cls):
        """Load settings common to all classes"""
        interfaces = ni.interfaces()
        cls.commotion_client_ip = 0

        if cls.commotion_client_ip == 0:
            for iface in interfaces:
                try:
                    if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
                        print iface + " has a valid Commotion IP address: " \
                            + ni.ifaddresses(iface)[2][0]['addr']
                        cls.commotion_client_ip = \
                            ni.ifaddresses(iface)[2][0]['addr']
                    else:
                        print iface + " not valid"
                except KeyError:
                    print iface + " has been disconnected"
                    continue

        if cls.commotion_client_ip == 0:
            error("No valid Commotion IP address found")
        else:
            # Use client IP address to determine node's public IP
            cls.commotion_node_ip = re.sub(r"(\d+)$", '1',
                                           cls.commotion_client_ip)

    @classmethod
    def load_browser(cls, browser, profile):
        """Init browser with proper profile"""
        # Move profiles to subclasses
        cls.ff_admin = webdriver.FirefoxProfile()
        cls.ff_admin.accept_untrusted_certs = True

        cls.profiles = {"default": None, "firefox_admin": cls.ff_admin}
        cls.browsers = {"firefox": webdriver.Firefox(cls.profiles[profile])}

        return cls.browsers[browser]

    @classmethod
    def tearDownClass(cls):
        """Clear all superclass settings"""
        cls.commotion_client_ip = 0
        cls.profiles = []
        cls.browsers = []
        logging.info("CRInputTestCase destroyed")


class TestCRUserFunctions(CRInputTestCase):
    """Test functions as unprivileged user"""

    def setUp(self):
        """Set up browser"""
        self.driver = self.load_browser("firefox", "default")

    @unittest.skipIf(1 == 1,
                     "Skip if wlan0 provides commotion ip \
                     and eth0 is in use")
    def test_thisnode(self):
        """Test thisnode dns resolution"""
        # SKIP THIS TEST if wlan0 provides commotion ip and eth0 is in use
        _sd = self.driver
        _sd.get('https://thisnode')
        WebDriverWait(_sd, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(_sd.find_element_by_id("device"))

    def test_ip_address(self):
        """Test ip-only connection"""
        _sd = self.driver
        _sd.get('https://' + self.commotion_node_ip)
        WebDriverWait(_sd, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(_sd.find_element_by_id("device"))

    def tearDown(self):
        """Quit test browser instance"""
        self.driver.quit()
        logging.info("Browser instance destroyed")


class TestCRAdminFunctions(CRInputTestCase):
    """Test functions as privileged user"""

    def setUp(self):
        """Set up browser to allow access to admin functions"""
        self.driver = self.load_browser("firefox", "firefox_admin")

    def test_require_admin_password(self):
        """
        Make sure a password is required for admin pages.
        Use admin profile to avoid DOM-less self-signed cert error.
        """
        _sd = self.driver
        url = 'https://' + self.commotion_node_ip + '/cgi-bin/luci/admin'
        _sd.get(url)
        WebDriverWait(_sd, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        self.assertTrue(_sd.find_element_by_class_name("cbi-input-user"))

    def test_log_in_fail(self):
        """Incorrect password should be rejected"""
        _sd = self.driver
        url = 'https://' + self.commotion_node_ip + '/cgi-bin/luci/admin'
        _sd.get(url)
        WebDriverWait(_sd, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        pw_field = _sd.find_element_by_id("focus_password")
        pw_field.send_keys("BADPASS\n")
        WebDriverWait(_sd, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error")))
        self.assertTrue(_sd.find_element_by_class_name("error"))

    def test_fuzz_admin_password_field(self):
        """Try to break password function"""
        # This should eventually replace test_log_in_fail
        _sd = self.driver
        url = 'https://' + self.commotion_node_ip + '/cgi-bin/luci/admin'
        _sd.get(url)
        WebDriverWait(_sd, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        # fuzz = gen_fuzz(params)
        # for garbage in fuzz:
        #       pw_field = _sd.find_element_by_id("focus_password")
        #       pw_field.send_keys(garbage)
        #       WebDriverWait(d, 10).until(
        #           EC.presence_of_element_located((By.CLASS_NAME, "error")))
        #       seleniumVerifyTrue(_sd.find_element_by_class_name("error"))
        # assertTrue(noSeleniumVerifyFailures)

    def test_log_in_pass(self):
        """Correct password should be accepted"""
        _sd = self.driver
        url = 'https://' + self.commotion_node_ip + '/cgi-bin/luci/admin'
        _sd.get(url)
        WebDriverWait(_sd, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        _sd.find_element_by_id("focus_password").send_keys('asdf')
        # Should actually check for div.error
        WebDriverWait(_sd, 10).until(
            EC.presence_of_element_located((By.ID, "xhr_poll_status")))
        self.assertTrue(_sd.find_element_by_id("xhr_poll_status"))

    def tearDown(self):
        """Quit test browser instance"""
        self.driver.quit()
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
    BROWSER_SUITE = suite()
    RUNNER = unittest.TextTestRunner()
    RUNNER.run(BROWSER_SUITE)
