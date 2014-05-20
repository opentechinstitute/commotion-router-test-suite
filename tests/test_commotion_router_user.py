"""Sample automated test suite for commotion router's unprivileged functions.
   These are an inefficient use of selenium, but are included as examples.
"""

import unittest
import objects.browser as cbo
import objects.router.page.page as cpo


class TestFirefoxUnprivileged(cbo.CRBrowserTestContext):
    """Unittest child class for unprivileged functions"""

    #def test_require_admin_password(self):
        #"""
        #Make sure a password is required for admin pages.
        #Use admin profile to bypass DOM-less self-signed cert error.
        #Calls login page object.
        #"""
        #login = cpo.CRLoginPageObjects(self.browser)
        #self.assertTrue(login.password_required(self.browser))

    def test_default_no_user_apps(self):
        """
        By default, the router homepage should not allow unprivileged
        users to add applications.
        Calls homepage object.
        """
        home = cpo.CRHomePageObjects(self.browser)
        self.assertFalse(home.users_can_add_apps(self.browser))


if __name__ == "__main__":
    # This is probably wrong
    def suite():
        """Gather all tests from this module into a test suite."""
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(TestFirefoxUnprivileged))
        return test_suite
    # Fix logging
    # https://stackoverflow.com/questions/3347019/\
    #    how-can-one-use-the-logging-module-in-python-with-the-unittest-module
    browser_suite = suite()
    runner = unittest.TextTestRunner()
    runner.run(browser_suite)
