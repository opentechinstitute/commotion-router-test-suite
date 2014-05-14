"""Collected page objects for Commotion Router web UI.
    Individual page elements are contained in xelements.py files.
"""

import commotiontestobjects.commotionrouterobjects.routerobjects as cro
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 

locators = {
    "login": {
        "password": "focus_password",
    }
}


class CRCommonPageObjects(object):
    """Page objects common to all Commotion Router pages"""

    def __init__(self):
        """Set page within context of router."""
        page_url = None
        __sb = None
        commotion_node_ip = None


    # This is dumb and duplicative. We only need node_ip.
    __, commotion_client_ip = cro.get_commotion_client_ip()
    commotion_node_ip = cro.get_commotion_node_ip(commotion_client_ip)


    def _verify_correct_page(self, __sb, page_url):
        """Sanity check defined page url against url in browser"""
        __sb.get(page_url)
        
        # Wait for known-good page element
        self.wait_for_page_load(__sb)

        try:
            # this assert may not work as expected
            assert (__sb.current_url == page_url) is True
            print __sb.current_url + " matches " + page_url
        except AssertionError:
            print "Rendered url %s does not match expected url %s" % (
                    __sb.current_url, page_url)

 
    def wait_for_page_load(self, __sb):
        """Tell selenium to wait for locator before proceeding"""
        print "Waiting for presence of known-good page element"
        try:
            WebDriverWait(__sb, 10).until(
                EC.presence_of_element_located((By.ID, "device")))
        except:
            message = "Page element 'device' not found!"
            print message
            raise message
        else:
            return True

    # Example
    # From http://justinlilly.com/python/selenium-page-object-pattern-\
    #    -the-key-to-maintainable-tests.html
    # These are currently handled in tests and browserobjects
    #
    #def fill_form_by_css(self, form_css, value):
        #elem = self.driver.find(form_css)
        #elem.send_keys(value)

    #def fill_form_by_id(self, form_element_id, value):
        #return self.fill_form_by_css('#%s' % form_element_id, value)

    #def navigate(self):
        #self.driver.get(self.url)
    # End example

    # thisnode url
    # Header
    # Footer
    # Body


class CRHomePageObjects(CRCommonPageObjects):
    """Objects found on Commotion Router's default landing page"""
    pass
#    page_url = netinfo.commotion_node_ip + '/cgi-bin/luci'


class CRLoginPageObjects(CRCommonPageObjects):
    """Page objects specific to Commotion Router login page.
        Note that the login page triggers a DOM-less cert error
    """

    def __init__(self, browser):
        super(CRLoginPageObjects, self).__init__()
        __sb = browser
        self.page_url = ('https://' + CRCommonPageObjects.commotion_node_ip
            + '/cgi-bin/luci/admin')
        self._verify_correct_page(__sb, self.page_url)

    # Username
    # Password
    def password_required(self):
        print "Waiting for", locators["login"]["password"]
        #try:
            #WebDriverWait(__sb, 10).until(
                #EC.presence_of_element_located(
                    #By.ID, locators["login"]["password"])
        #except:
            #print ("Password field locator "
                    #+ locators["login"]["password"]
                    #+ " not found")
        #else:
            #return True
        return True


    # Submit
    # Reset


class CRAdminPageObjects(CRCommonPageObjects):
    """Page objects accessible only to authenticated admin users"""
    # Side Nav
    ## Logout
    # URL stok (Note: This also allows csrf vuln)
    #page_url = 'https://' + self.netinfo.commotion_node_ip \
            #+ '/cgi-bin/luci/admin'
    pass
