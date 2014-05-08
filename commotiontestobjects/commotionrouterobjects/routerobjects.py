import sys
import netifaces as ni
import re

def error(message):
    #logging.error(message)
    sys.stderr.write("ERROR: %s\n" % message)
    sys.exit(1)
    
def getThisnodeIP(commotion_client_ip):
    interfaces = ni.interfaces()

    if commotion_client_ip == 0:
        for iface in interfaces:
            try:
                if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
                    print iface + " has a valid Commotion IP address: " + ni.ifaddresses(iface)[2][0]['addr']
                    commotion_client_ip = ni.ifaddresses(iface)[2][0]['addr']
                else:
                    print iface + " not valid"
            except KeyError:
                print iface + " has been disconnected"
                continue
    elif commotion_client_ip == '127.0.0.1':
        print "Working offline. No promises"
        commotion_node_ip = 'file:///home/areynold/Documents/Scripts/commotion-router-test-suite/offlinedocs'

    if commotion_client_ip == 0:
        # this should raise an exception insstead
        error("No valid Commotion IP address found")
    else:
        # Use client IP address to determine node's public IP
        commotion_node_ip = re.sub(r"(\d+)$", '1', commotion_client_ip)
        return commotion_client_ip, commotion_node_ip