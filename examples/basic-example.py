#!/usr/bin/python

###
### Quick Example Script
###
### Run script after connecting to a commotion AP
###
### . Script will check all interfaces for commotion lease
### . Script will open a web browser (Firefox)
### . Browser will try to connect to thisnode
### . If thisnode fails, browser will try node IP address
### . Print commotion version described in credits

# DEBUG
from pprint import pprint

import netifaces as ni
import sys
#import logging
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import unittest

def error(message):
        #logging.error('error: ', message)
        sys.stderr.write("error: %s\n" % message)
        sys.exit(1)


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

# Create a new instance of the firefox driver
driver = webdriver.Firefox()

# go to the node home page
driver.get("https://thisnode")

# Check for the Commotion logo
try:
	WebDriverWait(driver, 10).until(
		EC.presence_of_element_located(By.ID, "device"))
except:
	print 'https://thisnode does not resolve. Trying ' + commotion_node_ip
	driver.get(commotion_node_ip)
else:
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located(By.ID, "device"))
	assert element
finally:
	print driver.title

credits = driver.find_element_by_class_name('credits')
print credits.get_attribute('innerHTML')
commotion_version = re.search("Commotion Router Release (\w+\W+)+", credits.get_attribute('innerHTML')).group()
commotion_version = re.sub(r"(\s+)$", '', commotion_version)
print commotion_version
