import unittest
import netifaces as ni
import sys
#import logging
import re
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# DEBUG
from pprint import pprint

def error(message):
        #logging.error('error: ', message)
        sys.stderr.write("error: %s\n" % message)
        sys.exit(1)

def GetLease():
	# Check for Commotion DHCP lease
	interfaces = ni.interfaces()
	commotion_client_ip = 0
	for iface in interfaces:
		try: 
			if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
				print iface + " has a valid Commotion IP address: " + ni.ifaddresses(iface)[2][0]['addr']
				commotion_client_ip = ni.ifaddresses(iface)[2][0]['addr']
			else:
				print iface + " not valid"
		except KeyError:
			print iface + " has been disconnected"
			pass

	if commotion_client_ip == 0:
		error("No valid Commotion IP address found")
	else:
		# Use client IP address to determine node's public IP
		commotion_node_ip = re.sub(r"(\d+)$", '1', commotion_client_ip)

	return commotion_node_ip


browsers = {"firefox": webdriver.Firefox, "ie": webdriver.Ie, "chrome": webdriver.Chrome, "safari": webdriver.Safari}

class TestCRInputs(unittest.TestCase):

# Add profile/non-profile subclasses to deal with Self-Signed Cert error
# https://stackoverflow.com/questions/21884004/unittest-data-from-setupclass-to-setup?rq=1
# https://stackoverflow.com/questions/14044474/python-unittest-setupclass-is-giving-me-trouble-why-cant-i-inherit-like-t
#
# Organize better
# https://docs.python.org/dev/library/unittest.html
# https://stackoverflow.com/questions/12011091/trying-to-implement-python-testsuite

	def setUp(self):
		self.driver = browser()
		# This section should eventually be broken out into it's own test
		self.driver.thisnode = 'https://thisnode'
# Change this to a basic DOM check
		self.driver.get(self.driver.thisnode)
		try:
        		WebDriverWait(self.driver, 10).until(
                		EC.presence_of_element_located(By.ID, "device"))
		except:
        		print 'https://thisnode does not resolve.'
			print 'Fetching node IP address...'
			commotion_node_ip = GetLease()
			print 'Trying ' + commotion_node_ip
        		self.driver.thisnode = 'https://' + commotion_node_ip
			self.driver.get(self.driver.thisnode)
		else:
        		element = WebDriverWait(driver, 10).until(
                		EC.presence_of_element_located(By.ID, "device"))
        		assert element
		finally:
        		print self.driver.title
			print self.driver.thisnode

#	def test_something(self):
#		d = self.driver
#		d.refresh()

# Change this to a version check or something
	def test_title(self):
		d = self.driver
		d.get(d.thisnode)
		assert d.title

# Run without profile to test for Self-Signed Cert error

# Run with profile to test Admin functions

	def tearDown(self):
		self.driver.quit()

if __name__ == "__main__":
	browsername = "firefox"
	browser = browsers[browsername]

	suite = unittest.TestLoader().loadTestsFromTestCase(TestCRInputs)
	unittest.TextTestRunner().run(suite)
