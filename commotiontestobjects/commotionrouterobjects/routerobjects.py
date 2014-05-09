"""Test components specific to Commotion Routers"""
from commotiontestobjects.util import error
import bunch
import netifaces as ni
import re


def get_net_info(object):
    """Create object-like dict for netinfo"""
    if hasattr(object, 'interfaces') is False:
        object = bunch.Bunch(interfaces=ni.interfaces())

    if hasattr(object, "commotion_client_ip") is False:
        for iface in object.interfaces:
            try:
                if ni.ifaddresses(iface)[2][0]['addr'].startswith('10.'):
                    print iface + " has a valid Commotion IP address: " \
                        + ni.ifaddresses(iface)[2][0]['addr']
                    object = bunch.Bunch(commotion_client_ip=
                                         ni.ifaddresses(iface)[2][0]['addr'])
                else:
                    object.interfaces = bunch.Bunch(iface=False)
                    print iface + " not valid"
            except KeyError:
                object.interfaces = bunch.Bunch(iface=True)
                print iface + " has been disconnected"
                continue

    if getattr(object, "commotion_client_ip") is False:
        # this should raise an exception instead
        error("No valid Commotion IP address found")
        raise "No valid Commotion IP address found"
    else:
        # Use client IP address to determine node's public IP
        object = bunch.Bunch(commotion_node_ip=
                             re.sub(r"(\d+)$", '1',
                                    object.commotion_client_ip))

    return object
