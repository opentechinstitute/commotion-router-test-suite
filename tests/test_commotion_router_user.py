"""Sample automated test suite for commotion router's unprivileged functions.
    Partially broken.
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
import commotiontestobjects.browserobjects as cbo
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestCRUserFunctions(cbo.CRBrowserTestContext):
    """Unittest child class for unprivileged functions"""

    def test_ip_address(self):
        """Test ip-only connection"""
        __sb = self.browser
        
        __sb.get('https://' + self.netinfo.commotion_node_ip)
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(__sb.find_element_by_id("device"))

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


class TestCRAdminFunctions(cbo.CRBrowserTestContext):
    """Test admin functions. Note browser profile change"""

    profile = "firefox_admin"

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


if __name__ == "__main__":
    # This is probably wrong
    def suite():
        """Gather all tests from this module into a test suite."""
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(cbo.CRBrowserTestContext))
        test_suite.addTest(unittest.makeSuite(TestCRUserFunctions))
        test_suite.addTest(unittest.makeSuite(TestCRAdminFunctions))
        return test_suite
    # Fix logging
    # https://stackoverflow.com/questions/3347019/\
    #    how-can-one-use-the-logging-module-in-python-with-the-unittest-module
    browser_suite = suite()
    runner = unittest.TextTestRunner()
    runner.run(browser_suite)
