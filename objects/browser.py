"""Profiles and browser definitions for use in unit tests"""
import unittest
import objects.router.router as cro
from selenium import webdriver

class BrowserTestContext(unittest.TestCase):
    """Browser config and request methods for live commotion router testing"""

    browser = "firefox"
    profile = "default"

    @classmethod
    def setUpClass(cls):
        """Get information about net interfaces and target commotion node
            This may need to move to pageobjects __init__
        """
        cls.netinfo = {}
        cls.netinfo = cro.get_net_info()

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

    def setUp(self):
        """Set up browser"""
        self.browser = self.load_browser(self.browser, self.profile)

    def tearDown(self):
        """Clean up test instance"""
        self.browser.quit()

### Move request_browser and init_profile into BrowserTestContext
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
