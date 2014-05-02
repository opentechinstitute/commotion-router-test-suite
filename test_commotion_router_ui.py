import unittest
import netifaces as ni
import sys
#import logging
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
	def setUp(self):
		self.driver = browser()
		# This section should eventually be broken out into it's own test
		self.driver.thisnode = self.driver.get("https://thisnode")
		try:
        		WebDriverWait(self.driver, 10).until(
                		EC.presence_of_element_located(By.ID, "device"))
		except:
        		print 'https://thisnode does not resolve.'
			print 'Fetching node IP address...'
			commotion_node_ip = GetLease()
			print 'Trying ' + commotion_node_ip
        		self.driver.thisnode = self.driver.get(commotion_node_ip)
		else:
        		element = WebDriverWait(driver, 10).until(
                		EC.presence_of_element_located(By.ID, "device"))
        		assert element
		finally:
        		print driver.title
			print self.driver.thisnode

#	def test_something(self):
#		d = self.driver
#		
#		d.refresh()
#	def test_page_load

	def tearDown(self):
		self.driver.quit()

if __name__ == "__main__":
	browsername = "firefox"
	browser = browsers[browsername]

	suite = unittest.TestLoader().loadTestsFromTestCase(TestCRInputs)
	unittest.TextTestRunner().run(suite)
