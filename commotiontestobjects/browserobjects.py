"""Profiles and browser definitions for use in unit tests"""
import unittest
import logging
import commotiontestobjects.commotionrouterobjects.routerobjects as cro
from selenium import webdriver

class CRBrowserTestContext(unittest.TestCase):
    """Browser config and request methods for live commotion router testing"""

    browser = "firefox"
    profile = "default"

    logging.basicConfig(filename='logs/test_commotion_router_ui.log',
                        level=logging.INFO)
    logging.warning("Specify path to log directory")
    logging.warning("This test suite needs a UI map!")

    @classmethod
    def setUpClass(cls):
        """Get information about net interfaces and target commotion node
            This may need to move to pageobjects __init__
        """
        cls.netinfo = {}
        cls.netinfo = cro.get_net_info(cls.netinfo)

    @classmethod
    def load_browser(cls, browser, profile):
        """
        Pass request to browser generation function with desired browser
        and profile type
        """
        browser = request_browser(browser, profile)
        return browser

    @classmethod
    def tearDownClass(cls):
        #cls.netinfo = {}
        #cls.profile = None
        cls.browser = None
        logging.info("CRBrowserTestContext destroyed")

    def setUp(self):
        """Set up browser"""
        self.browser = self.load_browser(self.browser, self.profile)
        
        # Uncomment when browser.test_url has been added to page objects
        #self.browser.get(self.browser.test_url)

    def tearDown(self):
        """Clean up test instance"""
        self.browser.quit()
        logging.info("Browser instance destroyed")

### Move request_browser and init_profile into CRBrowserTestContext 
def request_browser(req_browser, req_profile):
    """Just a wrapper for the browser init functions"""
    __profile = None
    # Fetch profile
    __profile = init_profile(req_profile)

    # Define browser start methods
    browsers = {"firefox": webdriver.Firefox(__profile)}

    # Init browser
    browser = browsers[req_browser]

    return browser


def init_profile(req_profile):
    """Build selenium browser profile from browser/privilege type"""
    __profile = None
    # This could be made cleaner

    # Firefox Admin Profile
    ff_admin = webdriver.FirefoxProfile()
    ff_admin.accept_untrusted_certs = True

    # Profiles dict
    profiles = {"default": None, "firefox_admin": ff_admin}

    __profile = profiles[req_profile]

    # Select and return proper profile
    return __profile
