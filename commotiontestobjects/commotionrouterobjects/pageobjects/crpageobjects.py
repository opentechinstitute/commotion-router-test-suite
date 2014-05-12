"""Collected page objects for Commotion Router web UI.
    Individual page elements are contained in xelements.py files.
"""

class CRCommonPageObjects(object):
    """Page objects common to all Commotion Router pages"""

    thisnode = None
    

    # thisnode url
    thisnode = self.driver.netinfo.commotion_node_ip
    # Header
    # Footer
    # Body
    pass


class CRLoginPageObjects(CRCommonPageObjects):
    """Page objects specific to Commotion Router login page.
        Note that the login page triggers a DOM-less cert error
    """
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
