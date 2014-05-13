"""Sample automated test suite for commotion router's unprivileged functions.
    Most of these are an inefficient use of selenium, 
    but are included as examples.
"""

import unittest
import commotiontestobjects.browserobjects as cbo
import commotiontestobjects.commotionrouterobjects.pageobjects.crpageobjects as cpo


class TestMini(cbo.CRBrowserTestContext):
    """just a proof of concept"""
    profile = "firefox_admin"

    def test_require_admin_password(self):
        """
        Make sure a password is required for admin pages.
        Use admin profile to avoid DOM-less self-signed cert error.
        """
        login = cpo.CRLoginPageObjects(self.browser)
        test_url = self.netinfo.commotion_node_ip + '/cgi-bin/luci/admin'
        self.assertEqual(login.page_url, test_url)

        #url = 'https://' + self.netinfo.commotion_node_ip \
            #+ '/cgi-bin/luci/admin'
        #__sb.get(url)
        #WebDriverWait(__sb, 10).until(
            #EC.presence_of_element_located((By.CLASS_NAME, "cbi-input-user")))
        #self.assertTrue(__sb.find_element_by_class_name("cbi-input-user"))


if __name__ == "__main__":
    # This is probably wrong
    def suite():
        """Gather all tests from this module into a test suite."""
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(cbo.CRBrowserTestContext))
        test_suite.addTest(unittest.makeSuite(TestMini))
        return test_suite
    # Fix logging
    # https://stackoverflow.com/questions/3347019/\
    #    how-can-one-use-the-logging-module-in-python-with-the-unittest-module
    browser_suite = suite()
    runner = unittest.TextTestRunner()
    runner.run(browser_suite)
