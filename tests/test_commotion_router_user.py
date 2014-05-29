"""Sample automated test suite for commotion router's unprivileged functions.
   These are an inefficient use of selenium, but are included as examples.
"""

import unittest
import objects.browser as cbo
import objects.router.page.page as cpo


class TestFirefoxUnprivileged(cbo.BrowserTestContext):
    """Unittest child class for unprivileged functions"""

    def test_show_correct_version(self):
        """Check the footer for the current Commotion revision"""
        home = cpo.CRHomePage(self.browser)
        test_rev = "Commotion Router Release 1.1rc2"
        # This should return the footer string instead, then assertEqual
        self.assertTrue(home.show_current_rev(self.browser, test_rev),
                        'Incorrect revision in footer')

    def test_default_no_user_apps(self):
        """
        By default, the router homepage should not allow unprivileged
        users to add applications.
        Calls homepage object.
        """
        home = cpo.CRHomePage(self.browser)
        self.assertFalse(home.users_can_add_apps(self.browser),
                         'Default app permissions incorrect')


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
    BROWSER_SUITE = suite()
    RUNNER = unittest.TextTestRunner()
    RUNNER.run(BROWSER_SUITE)
