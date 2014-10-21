"""Sample automated test suite for commotion router's unprivileged functions.
    Most of these are an inefficient use of selenium,
    but are included as examples.
"""

import unittest
import objects.browser as cbo
import objects.router.page.page as cpo
import configparser
import pytest


class TestFirefoxAdmin(cbo.BrowserTestContext):
    """Tests of privileged Commotion Router web functions"""

    # Override default profile (None)
    profile = "firefox_admin"

    # Set router username and password
    config = configparser.ConfigParser()
    config.read('pytest.ini')
    admin_password = config.get('admin_common', 'admin_password')
    admin_user = config.get('admin_common', 'admin_user')

    def test_require_admin_password(self):
        """
        Make sure a password is required for admin pages.
        Use admin profile to bypass DOM-less self-signed cert error.
        Calls login page object.
        """
        login = cpo.CRLoginPage(self.browser)
        self.assertTrue(login.password_required(self.browser),
                        'Admin pages not password protected')

    def test_login_fail(self):
        """
        Incorrect password should result in error message.
        Calls login page object
        """
        password = "garbage\n"
        login = cpo.CRLoginPage(self.browser)
        self.assertTrue(
            login.incorrect_pass_returns_error(self.browser, password),\
                'Failed login does not return error'
            )

    @pytest.mark.xfail(admin_password == "ChangeMe",
                       reason="Will fail until correct pass set in pytest.ini")
    def test_login_succeed(self):
        """
        Correct password should allow access to admin functions.
        Password should be defined at runtime
        """
        login = cpo.CRLoginPage(self.browser)
        self.assertTrue(
            login.correct_pass_allows_access(self.browser, self.admin_password),\
            'Login form does not allow access on correct password'
            )

    def test_login_input_validation(self):
        """
        Pass bad strings to login page in order to break password function.
        password list is populated from user-defined external strings file.
        """
        from objects.malicious_strings import MALICIOUS_STRINGS
        buggy_strings = []
        for _, malicious in enumerate(MALICIOUS_STRINGS):
            # Need to reset page after each attempt
            # Otherwise pw fail error stays on screen
            login = cpo.CRLoginPage(self.browser)
            print(malicious)
            # This test needs revision.
            # 1. exception will probably end the test early
            try:
                self.assertTrue(
                    login.incorrect_pass_returns_error(
                        self.browser, malicious),\
                        'Password form does not validate strings correctly'
                    )
            except ValueError:
                buggy_strings.append(malicious)
                print("%s causes login form problems" % malicious)

        self.assertEqual(list(buggy_strings), [])
