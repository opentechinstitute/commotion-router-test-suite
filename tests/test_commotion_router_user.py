"""Sample automated test suite for commotion router's unprivileged functions.
   These are an inefficient use of selenium, but are included as examples.
"""

import unittest
import objects.browser as cbo
import objects.router.page.page as cpo


class TestFirefoxUnprivileged(cbo.CRBrowserTestContext):
    """Unittest child class for unprivileged functions"""

    def test_ip_address(self):
        """Test ip-only connection"""
        __sb = self.browser

        __sb.get('https://' + self.netinfo.commotion_node_ip)
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(__sb.find_element_by_id("device"))

    @unittest.skipIf(1 == 1,
                     "Skip if wlan0 provides commotion ip and eth0 is in use")
    def test_thisnode(self):
        """Test thisnode dns resolution"""
        # SKIP THIS TEST if wlan0 provides commotion ip and eth0 is in use
        __sb = self.browser
        __sb.get('https://thisnode')
        WebDriverWait(__sb, 10).until(
            EC.presence_of_element_located((By.ID, "device")))
        self.assertTrue(__sb.find_element_by_id("device"))


if __name__ == "__main__":
    # This is probably wrong
    def suite():
        """Gather all tests from this module into a test suite."""
        test_suite = unittest.TestSuite()
        test_suite.addTest(unittest.makeSuite(cbo.CRBrowserTestContext))
        test_suite.addTest(unittest.makeSuite(TestCRUserFunctions))
        test_suite.addTest(unittest.makeSuite(TestCRAdminFunctions))
        return test_suite
    # Fix logging
    # https://stackoverflow.com/questions/3347019/\
    #    how-can-one-use-the-logging-module-in-python-with-the-unittest-module
    browser_suite = suite()
    runner = unittest.TextTestRunner()
    runner.run(browser_suite)
