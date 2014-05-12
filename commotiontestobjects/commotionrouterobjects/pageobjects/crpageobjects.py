"""Collected page objects for Commotion Router web UI.
    Individual page elements are contained in xelements.py files.
"""

import commotiontestobjects.browserobjects
import commotiontestobjects.commotionrouterobjects.routerobjects as cro


class CRCommonPageObjects(object):
    """Page objects common to all Commotion Router pages"""

    # page_url will be set by individual pages
    # Could prepopulate with thisnode or commotion_node_ip
    # but these won't actually match when rendered
    page_url = None
    netinfo = None
    browser = None

    def __init__(self, browser):
        """Set page within context of router. Import browser"""
        self.netinfo = cro.get_net_info(self)
        __sb = browser

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
#    page_url = netinfo.commotion_node_ip + '/cgi-bin/luci'
    # Username
    # Password
    # Submit
    # Reset
    pass


class CRAdminPageObjects(CRCommonPageObjects):
    """Page objects accessible only to authenticated admin users"""
    # Side Nav
    # URL stok (Note: This also allows csrf vuln)
    pass
