#!/usr/bin/python

# used to check ip address
import netifaces as ni

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Check for DHCP lease
interfaces = ni.interfaces()
for iface in interfaces:
	if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
		print iface + " has a valid Commotion IP address: " + ni.ifaddresses(iface)[2][0]['addr']
	else:
		print iface + " not valid"



# Create a new instance of the firefox driver
#driver = webdriver.Firefox()

# go to the node home page
#driver.get("https://thisnode")
#
## the page is ajaxy so the title is originally this:
#print driver.title
#
##driver.
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
