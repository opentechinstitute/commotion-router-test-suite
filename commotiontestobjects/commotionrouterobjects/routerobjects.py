import sys
import bunch
import netifaces as ni
import re

def error(message):
    #logging.error(message)
    sys.stderr.write("ERROR: %s\n" % message)
    sys.exit(1)
    
def getNetInfo(object):
    """Create object-like dict for netinfo"""
    
    # Need to check for existing attributes first
    object = bunch.Bunch(interfaces = ni.interfaces())

    #if hasattr(object, commotion_client_ip) is False:
    for iface in object.interfaces:
        try:
            if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
                print iface + " has a valid Commotion IP address: " + ni.ifaddresses(iface)[2][0]['addr']
                object = bunch.Bunch(commotion_client_ip = ni.ifaddresses(iface)[2][0]['addr'])
            else:
                object.interfaces = bunch.Bunch(iface = False)
                print iface + " not valid"
        except KeyError:
            object.interfaces = bunch.Bunch(iface = True)
            print iface + " has been disconnected"
            continue
            
    if object.commotion_client_ip is None:
        # this should raise an exception instead
        error("No valid Commotion IP address found")
        raise "No valid Commotion IP address found"
    else:
        # Use client IP address to determine node's public IP
        object.commotion_node_ip = re.sub(r"(\d+)$", '1', object.commotion_client_ip)
    
    return object
