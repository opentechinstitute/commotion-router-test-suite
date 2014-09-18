"""Collected page objects for Commotion Router web UI.
    Individual page elements are contained in xelements.py files.
"""

import objects.router.router as cro
import objects.exceptions as exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# Core identifiers for each page.
LOCATORS = {
    "common": {
        "commotion_logo": "device", # ID
        "version": "credits", # Class - requires add'l filtering
    },
    "login": {
        "username_field": "username", # Name
        "password_field": "focus_password", # ID
        "error": "error", # Class
        "submit": "cbi-button-apply", # Class
        "reset": "cbi-button-reset", # Class
    },
    "home": {
        "apps-header": "appsH2", # Class
        "user-add-app": "add_app", # ID
    },
    "admin": {
        "url-stok": False,
        "logout": False,
    },
}


class CRCommonPage(object):
    """Page objects common to all Commotion Router pages"""

    def __init__(self):
        """Set page within context of router."""
        page_url = None
        __sb = None
        commotion_node_ip = None


    # This is dumb and duplicative. We only need node_ip.
    try:
        _, commotion_client_ip = cro.get_commotion_client_ip()
    except exceptions.CommotionIPError as args:
        print(args)
    else:
        if commotion_client_ip is not None:
            commotion_node_ip = cro.get_commotion_node_ip(commotion_client_ip)


    def _verify_correct_page(self, __sb, page_url):
        """Sanity check defined page url against url in browser"""
        __sb.get(page_url)

        # Wait for known-good page element
        self.wait_for_page_load(__sb)

        try:
            # this assert may not work as expected
            assert (__sb.current_url == page_url) is True
            print(__sb.current_url + " matches " + page_url)
        except AssertionError:
            print("Rendered url %s does not match expected url %s" % (
                __sb.current_url, page_url
                ))


    def wait_for_page_load(self, __sb):
        """Tell selenium to wait for locator before proceeding"""
        print("Waiting for presence of known-good page element")
        try:
            WebDriverWait(__sb, 10).until(
                EC.presence_of_element_located((By.ID, "device")))
        except NoSuchElementException:
            message = "Page element 'device' not found!"
            print(message)
            raise Exception(message)
        else:
            print("%s loaded successfully" % __sb.current_url)

    def wait_for_element_of_type(self, __sb, etype, element):
        """
        Tell selenium to wait for a specific locator of specific type
        before proceeding.

        Valid types: ID, CLASS_NAME, CSS_SELECTOR, LINK_TEXT, NAME,
            PARTIAL_LINK_TEXT, TAG_NAME, XPATH
        """
        print("Waiting for %s, type %s" % (element, etype))
        try:
            WebDriverWait(__sb, 10).until(
                EC.presence_of_element_located((
                    (
                        getattr(By, etype)), element
                    )))
        except NoSuchElementException:
            print("Page element %s of type %s not found!" % (
                element, etype
                ))
        else:
            print("Page element %s found." % element)
            return True


    # thisnode url
    # Header
    # Footer
    # Body


class CRHomePage(CRCommonPage):
    """Objects found on Commotion Router's default landing page"""
    def __init__(self, browser):
        super(CRHomePage, self).__init__()
        __sb = browser
        self.page_url = (
            'https://' + CRCommonPage.commotion_node_ip + '/cgi-bin/luci'
            )
        self._verify_correct_page(__sb, self.page_url)


    def show_current_rev(self, __sb, test_rev):
        """Check page footer for commotion version number.
        This is actually a common object but common class
        isn't written to accept tests."""
        print("Checking footer for correct Commotion Revision")
        CRCommonPage.wait_for_element_of_type(
            self, __sb, "CLASS_NAME", LOCATORS["common"]["version"]
            )
        print("Comparing versions")
        page_rev = __sb.find_element_by_class_name(LOCATORS["common"]
                                                   ["version"])
        # Could also use page_rev.text.endswith(test_rev)
        if test_rev not in page_rev.text:
            print("Footer version %s does not match test version %s", (
                page_rev.text, test_rev))
            return False
        else:
            return True


    def users_can_add_apps(self, __sb):
        """When enabled, unprivileged users can add apps from the homepage"""
        print("Checking for app add button...")
        try:
            __sb.find_element_by_id(LOCATORS["home"]["user-add-app"])
        except NoSuchElementException:
            return False
        else:
            print("Users can add applications from the homepage")
            return True


class CRLoginPage(CRCommonPage):
    """Page objects specific to Commotion Router login page.
        Note that the login page triggers a DOM-less cert error
    """

    def __init__(self, browser):
        super(CRLoginPage, self).__init__()
        __sb = browser
        self.page_url = (
            'https://' + CRCommonPage.commotion_node_ip + '/cgi-bin/luci/admin'
            )
        self._verify_correct_page(__sb, self.page_url)

    def password_required(self, __sb):
        """
        Admin pages should require a password if stok url token is not present.
        """
        print("Checking for password field...")
        try:
            __sb.find_element_by_id(LOCATORS["login"]["password_field"])
        except NoSuchElementException:
            print("Login page element %s not found" % (
                LOCATORS["login"]["password_field"]
                ))
            return False
        else:
            print("Login page requires a password")
            return True

    def incorrect_pass_returns_error(self, __sb, password):
        """The login form should reject incorrect passwords"""
        print("Testing user-supplied password")
        __sb.find_element_by_id(
            LOCATORS["login"]["password_field"]
            ).send_keys(password)

        if "\n" not in password:
            # Click submit if password doesn't have a newline
            __sb.find_element_by_class_name("cbi-button-apply").click()

        CRCommonPage.wait_for_element_of_type(
            self, __sb, "CLASS_NAME", LOCATORS["login"]["error"]
            )
        # Rewrite as try/except NoSuchElementException/else
        if __sb.find_element_by_class_name(LOCATORS["login"]["error"]).is_displayed():
            print("Login page displays error message on incorrect password")
            return True
        else:
            print("Login page does not display error message " \
                "on incorrect password")
            return False

    def correct_pass_allows_access(self, __sb, password):
        """
        Correct password in login form should allow access to admin pages
        """
        pass



class CRAdminPage(CRCommonPage):
    """Page objects accessible only to authenticated admin users"""
    # Side Nav
    ## Logout
    # URL stok (Note: This also allows csrf vuln)
    #page_url = 'https://' + self.netinfo.commotion_node_ip \
            #+ '/cgi-bin/luci/admin'
    pass
