"""Sample automated test suite for commotion router's unprivileged functions.
    Most of these are an inefficient use of selenium, 
    but are included as examples.
"""

import unittest
import objects.browser as cbo
import objects.router.page.page as cpo


class TestFirefoxAdmin(cbo.CRBrowserTestContext):
    """Tests of privileged Commotion Router web functions"""

    # Override default profile (None)
    profile = "firefox_admin"

    def test_require_admin_password(self):
        """
        Make sure a password is required for admin pages.
        Use admin profile to bypass DOM-less self-signed cert error.
        Calls login page object.
        """
        login = cpo.CRLoginPageObjects(self.browser)
        self.assertTrue(login.password_required(self.browser), 
                        'Admin pages not password protected')

    def test_login_fail(self):
        """
        Incorrect password should result in error message.
        Calls login page object
        """
        password = "garbage\n"
        login = cpo.CRLoginPageObjects(self.browser)
        self.assertTrue(login.incorrect_pass_returns_error(
            self.browser, password),
            'Failed login does not return error'
            )

    # Will fail until correct pass configured
    @unittest.expectedFailure
    def test_login_succeed(self):
        """
        Correct password should allow access to admin functions.
        Password should be defined at runtime
        """
        password = "garbage\n"
        login = cpo.CRLoginPageObjects(self.browser)
        self.assertTrue(login.correct_pass_allows_access(
            self.browser, password),
            'Login form does not allow access on correct password'
            )

    def test_login_input_validation(self):
        """
        Pass bad strings to login page in order to break password function.
        password list is populated from user-defined external strings file.
        """
        from objects.malicious_strings import MALICIOUS_STRINGS
        buggy_strings = []
        login = cpo.CRLoginPageObjects(self.browser)
        for _, malicious in enumerate(MALICIOUS_STRINGS):
            print malicious
            # Test each string. Save failures until the end
            try:
                self.assertTrue(login.incorrect_pass_returns_error(
                    self.browser, malicious),
                    'Password form does not validate strings correctly'
                )
            except ValueError:
                buggy_strings.append(malicious)
                print "%s causes login form problems" % malicious

        self.assertEqual(list(buggy_strings), [])



if __name__ == "__main__":
    # This is probably wrong
    def suite():
        """Gather all tests from this module into a test suite."""
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(cbo.CRBrowserTestContext))
        test_suite.addTest(unittest.makeSuite(TestFirefoxAdmin))
        return test_suite
    # Fix logging
    # https://stackoverflow.com/questions/3347019/how-can-one-use-the-logging-module-in-python-with-the-unittest-module
    BROWSER_SUITE = suite()
    RUNNER = unittest.TextTestRunner()
    RUNNER.run(BROWSER_SUITE)
