import unittest
import netifaces as ni
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

def error(message):
    logging.error(message)
    sys.stderr.write("ERROR: %s\n" % message)
    sys.exit(1)
    
class crInputTestCase(unittest.TestCase):
    """Setting defaults for live commotion router testing"""
    
    @classmethod
    def setUpClass(cls):
        interfaces = ni.interfaces()
        cls.commotion_client_ip = 0
        
        if cls.commotion_client_ip == 0:
            for iface in interfaces:
                try:
                    if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
                        print iface + " has a valid Commotion IP address: " + ni.ifaddresses(iface)[2][0]['addr']
                        cls.commotion_client_ip = ni.ifaddresses(iface)[2][0]['addr']
                    else:
                        print iface + " not valid"
                except KeyError:
                    print iface + " has been disconnected"
                    pass

        if cls.commotion_client_ip == 0:
            error("No valid Commotion IP address found")
        else:
            # Use client IP address to determine node's public IP
            cls.commotion_node_ip = re.sub(r"(\d+)$", '1', cls.commotion_client_ip)

    @classmethod
    def loadBrowser(cls, browser, profile):
        # Move profiles to subclasses
        cls.ff_admin = webdriver.FirefoxProfile()
        cls.ff_admin.accept_untrusted_certs = True

        cls.profiles = {"default":browser+"profile=None", "firefox_admin": cls.ff_admin}
        cls.browsers = {"firefox":"webdriver.Firefox("+cls.profiles[profile]+")", "chrome":"webdriver.Chrome("+cls.profiles[profile]+")"}

        print "Returning " + cls.browsers[browser]

        return cls.browsers[browser]

    @classmethod
    def tearDownClass(cls):
        """Forget everything about the browser"""
        cls.driver.quit()
        logging.info('Browser instance destroyed')
        print "Teardown complete"
        
class TestCRUserFunctions(crInputTestCase):
    def setUp(self):
        """Set up browser"""
        print self.commotion_node_ip
        self.driver = self.loadBrowser("firefox", "default")
        
    def test_thisnode(self):
        """Test thisnode dns resolution"""
        d = self.driver
        d.get('https://thisnode')
        assert d.title
        
    def test_ip_address(self):
        """Test ip-only connection"""
        d = self.driver
        d.get(commotion_node_ip)
        assert d.title
        
    def test_require_admin_password(self):
        """Make sure a password is required for admin pages"""
        d = self.driver
        d.get(d.thisnode + '/cgi-bin/luci/admin')
        assert d.MEAT
    
class TestCRAdminFunctions(crInputTestCase):
    def setUp(self):
        """Set up browser to allow access to admin functions"""
        print self.commotion_node_ip
        self.driver = self.loadBrowser("firefox", "firefox_admin")        

if __name__ == "__main__":
    # This is probably wrong
    def suite():
        """Gather all tests from this module into a test suite."""
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(crInputTestCase))
        test_suite.addTest(unittest.makeSuite(TestCRUserFunctions))
        test_suite.addTest(unittest.makeSuite(TestCRAdminFunctions))
        return test_suite
    
    browser_suite = suite()
    runner = unittest.TextTestRunner()
    runner.run(browser_suite)