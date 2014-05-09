from selenium import webdriver
from selenium.webdriver.firefox import firefox_profile

def requestBrowser(req_browser, req_profile):
    """Just a wrapper for the init functions"""
    _Profile = None
    # Fetch profile
    _Profile = initProfile(req_profile)
    
    # Define browser start methods
    browsers = {"firefox": webdriver.Firefox(_Profile)}

    # Init browser
    Browser = browsers[req_browser]

    return Browser

def initProfile(req_profile):
    _Profile = None
    # This could be made cleaner
    
    # Firefox Admin Profile
    ff_admin = webdriver.FirefoxProfile()
    ff_admin.accept_untrusted_certs = True

    # Profiles dict
    profiles = {"default": None, "firefox_admin": ff_admin}
    
    _Profile = profiles[req_profile]
    
    # Select and return proper profile
    return _Profile
