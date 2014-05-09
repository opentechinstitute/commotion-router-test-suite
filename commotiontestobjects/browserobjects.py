"""Profiles and browser definitions for use in unit tests"""
from selenium import webdriver
#from selenium.webdriver.firefox import firefox_profile


def request_browser(req_browser, req_profile):
    """Just a wrapper for the init functions"""
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
