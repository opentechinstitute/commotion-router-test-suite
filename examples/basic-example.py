#!/usr/bin/python

###
### Quick Example Script
###
### Run script after connecting to a commotion AP
###
### 1. Script will open a web browser
### 2. Browser will navigate to thisnode
### 3. Browser will check whether any apps are advertising
### 4. Browser will attempt to fetch a web page
### 5. Browser will report whether there's a gateway

import netifaces as ni
import sys
#import logging
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def error(message):
        #logging.error('error: ', message)
        sys.stderr.write("error: %s\n" % message)
        sys.exit(1)


# Check for Commotion DHCP lease
interfaces = ni.interfaces()
commotion_client_ip = 0
for iface in interfaces:
	# This line has trouble with interface disconnects
	if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
		print iface + " has a valid Commotion IP address: " + ni.ifaddresses(iface)[2][0]['addr']
		commotion_client_ip = ni.ifaddresses(iface)[2][0]['addr']
	else:
		print iface + " not valid"

if commotion_client_ip == 0:
	error("No valid Commotion IP address found")
else:
	commotion_node_ip = re.sub(r"(\d+)$", '1', commotion_client_ip)
	print commotion_node_ip

# Create a new instance of the firefox driver
#driver = webdriver.Firefox()
#
## go to the node home page
#driver.get("https://thisnode")
#try:
#	verify "LuCI" in driver.title
#else:
##print driver.title
#
#
## This is not actually an input element
##inputElement = driver.find_element_by_class_name("app")
## get_element_value
##
##if inputElement:
##	print str(inputElement)[1:-1]
##else:
##	print "No apps advertised\n"
##
#inputElement = driver.find_element_by_link_text("Administration")
#inputElement.click()
## This will fail on first run due to self-signed cert
## See http://fijiaaron.wordpress.com/2010/03/16/getting-past-untrusted-connections-on-self-signed-ssl-certs-using-selenium/
##try:
##	WebDriverWait(driver, 10).until(EC.presence_of_element_located("h2"))
###	print driver.title
#
##driver.quit()
### find the element with name attribute q (the search box)
##inputElement = driver.find_element_by_id("StreetAddressFrom")
##
### enter search terms
##inputElement.send_keys("1899 L St NW")
##
### find the element with name attribute q (the search box)
##inputElement = driver.find_element_by_id("StreetAddressTo")
##
### enter search terms
##inputElement.send_keys("College Park")
##
##
### sumbmit form (although google now searches without submitting)
##inputElement.submit()
##
##try:
##	# We have to wait for the page to refresh
##	WebDriverWait(driver, 10).until(EC.title_contains("Trip Planner"))
##	
##	# should see "meat - Google Search"
##	print driver.title
##
##finally:
#####	print "Meat\n!"

