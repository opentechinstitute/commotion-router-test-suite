# To do:
# Write Commotion-Router UI map for Selenium
# (See also Page Object Design Pattern)
# Write input fuzzers
# Write admin module
# Write logging functions

import unittest
#import netifaces as ni
import commotiontestobjects.commotionrouterobjects.routerobjects as cro
import sys
import logging
import re
from selenium import webdriver
from selenium.webdriver.firefox import firefox_profile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logging.basicConfig(filename='logs/test_commotion_router_ui.log',
                    level=logging.INFO)
logging.warning("Specify path to log directory")
logging.warning("This test suite needs a UI map!")

def error(message):
    logging.error(message)
    sys.stderr.write("ERROR: %s\n" % message)
    sys.exit(1)
    
class crInputTestCase(unittest.TestCase):
    """Setting defaults for live commotion router testing"""
    
    @classmethod
    def setUpClass(cls):
        cls.netinfo = {}
        cls.netinfo = cro.getNetInfo(cls.netinfo)

    @classmethod
    def loadBrowser(cls, browser, profile):
        # Move profiles to subclasses
        cls.ff_admin = webdriver.FirefoxProfile()
        cls.ff_admin.accept_untrusted_certs = True

        cls.profiles = {"default":None, "firefox_admin": cls.ff_admin}
        cls.browsers = {"firefox":webdriver.Firefox(cls.profiles[profile])}

        return cls.browsers[browser]
    
    @classmethod
    def tearDownClass(cls):
        cls.commotion_client_ip = 0
        cls.profiles = []
        cls.browsers = []
        logging.info("crInputTestCase destroyed")

#class TestOffline(crInputTestCase):
    #"""Offline mode for development use only"""
    #def setUp(self):
        #self.commotion_client_ip = '127.0.0.1'

    #def tearDown(self):
        #self.driver.quit()
        #logging.info("Browser instance destroyed")
        
class TestCRUserFunctions(crInputTestCase):
    def setUp(self):
        """Set up browser"""
        self.driver = self.loadBrowser("firefox", "default")
    
    @unittest.skipIf(1 == 1, "Skip if wlan0 provides commotion ip and eth0 is in use")
    def test_thisnode(self):
        """Test thisnode dns resolution"""
        # SKIP THIS TEST if wlan0 provides commotion ip and eth0 is in use
        d = self.driver
        d.get('https://thisnode')
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(d.find_element_by_id("device"))
        #assertIsNotNone(element)
        
    def test_ip_address(self):
        """Test ip-only connection"""
        d = self.driver
        d.get('https://' + self.commotion_node_ip)
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(d.find_element_by_id("device"))
        
    def tearDown(self):
        self.driver.quit()
        logging.info("Browser instance destroyed")
    
class TestCRAdminFunctions(crInputTestCase):
    def setUp(self):
        """Set up browser to allow access to admin functions"""
        self.driver = self.loadBrowser("firefox", "firefox_admin")        

    def test_require_admin_password(self):
        """Make sure a password is required for admin pages. Use admin profile to avoid DOM-less self-signed cert error."""
        d = self.driver
        url = 'https://' + self.commotion_node_ip + '/cgi-bin/luci/admin'
        d.get(url)
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        self.assertTrue(d.find_element_by_class_name("cbi-input-user"))
    
    def test_log_in_fail(self):
        d = self.driver
        url = 'https://' + self.commotion_node_ip + '/cgi-bin/luci/admin'
        d.get(url)
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        pw_field = d.find_element_by_id("focus_password")
        pw_field.send_keys("BADPASS\n")
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error")))
        self.assertTrue(d.find_element_by_class_name("error"))

    def test_fuzz_admin_password_field(self):
        # This should eventually replace test_log_in_fail
        d = self.driver
        url = 'https://' + self.commotion_node_ip + '/cgi-bin/luci/admin'
        d.get(url)
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        # fuzz = gen_fuzz(params)
        # for garbage in fuzz:
        #       pw_field = d.find_element_by_id("focus_password")
        #       pw_field.send_keys(garbage)
        #       WebDriverWait(d, 10).until(
        #           EC.presence_of_element_located((By.CLASS_NAME, "error")))
        #       seleniumVerifyTrue(d.find_element_by_class_name("error"))
        # assertTrue(noSeleniumVerifyFailures)


    def test_log_in_pass(self):
        d = self.driver
        url = 'https://' + self.commotion_node_ip + '/cgi-bin/luci/admin'
        d.get(url)
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        d.find_element_by_id("focus_password").send_keys('asdf')
        # Should actually check for div.error
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located((By.ID, "xhr_poll_status")))
        self.assertTrue(d.find_element_by_id("xhr_poll_status"))
    

    def tearDown(self):
        self.driver.quit()
        logging.info("Browser instance destroyed")
        
if __name__ == "__main__":
    # This is probably wrong
    def suite():
        """Gather all tests from this module into a test suite."""
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(crInputTestCase))
        test_suite.addTest(unittest.makeSuite(TestCRUserFunctions))
        test_suite.addTest(unittest.makeSuite(TestCRAdminFunctions))
        return test_suite
    # Fix logging
    # https://stackoverflow.com/questions/3347019/how-can-one-use-the-logging-module-in-python-with-the-unittest-module
    browser_suite = suite()
    runner = unittest.TextTestRunner()
    runner.run(browser_suite)
