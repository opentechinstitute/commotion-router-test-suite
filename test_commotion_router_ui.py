import unittest
import netifaces as ni
import sys
import logging
import re
from selenium import webdriver
from selenium.webdriver.firefox import firefox_profile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def error(message):
    logging.error('ERROR: ', message)
    sys.stderr.write("ERROR: %%s\n" % message)
    sys.exit(1)
    
class TestCRInputs(unittest.TestCase):
    """Defaults for live commotion router testing"""
    @classmethod
    def setUpClass(cls):
        cls.interfaces = ni.interfaces()
        cls.commotion_client_ip = 0
        
        if cls.commotion_client_ip == 0:
            for iface in cls.interfaces:
                try:
                    if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
                        print iface + " has a valid Commotion IP address: " + ni.ifaddresses(iface)[2][0]['addr']
                        cls.commotion_client_ip = ni.ifaddresses(iface)[2][0]['addr']
                    else:
                        print iface + " not valid"
                except KeyError:
                    print iface + " has been disconnected"
                    pass

        if cls.commotion_client_ip == 0:
            error("No valid Commotion IP address found")
        else:
            # Use client IP address to determine node's public IP
            cls.commotion_node_ip = re.sub(r"(\d+)$", '1', cls.commotion_client_ip)

    def setUp(self):
        """Set up browser"""
        print self.commotion_node_ip
        self.driver = browser()
        
    def test_thisnode(self):
        """Test thisnode dns resolution"""
        d = self.driver
        d.get('https://thisnode')
        assert d.title
        
    def test_ip_address(self):
        """Test ip-only connection"""
        d = self.driver
        d.get(self.commotion_node_ip)
        assert d.title
        
        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCRInputs)
    unittest.TextTestRunner().run(suite)