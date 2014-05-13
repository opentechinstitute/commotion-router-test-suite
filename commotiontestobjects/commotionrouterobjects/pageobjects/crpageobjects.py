"""Collected page objects for Commotion Router web UI.
    Individual page elements are contained in xelements.py files.
"""

import commotiontestobjects.browserobjects
import commotiontestobjects.commotionrouterobjects.routerobjects as cro
import netifaces as ni


class CRCommonPageObjects(object):
    """Page objects common to all Commotion Router pages"""

    def __init__(self):
        """Set page within context of router."""
        page_url = None
        __sb = None
        commotion_node_ip = None


    # This is dumb and duplicative
    _, commotion_client_ip = cro.get_commotion_client_ip()
    commotion_node_ip = cro.get_commotion_node_ip(commotion_client_ip)

    # page_url will be set by individual pages
    # Could prepopulate with thisnode or commotion_node_ip
    # but these won't actually match when rendered


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
        super(CRCommonPageObjects, self).__init__()
        __sb = browser

    page_url = 'https://' + CRCommonPageObjects.commotion_node_ip \
        + '/cgi-bin/luci/admin'
    # Username
    # Password
    # Submit
    # Reset


class CRAdminPageObjects(CRCommonPageObjects):
    """Page objects accessible only to authenticated admin users"""
    # Side Nav
    # URL stok (Note: This also allows csrf vuln)
    #page_url = 'https://' + self.netinfo.commotion_node_ip \
            #+ '/cgi-bin/luci/admin'
    pass
