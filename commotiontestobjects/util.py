import sys
#import logging

def error(message):
    """Basic error reporting function"""
    #logging.error(message)
    raise "ERROR: %s\n" % message
    sys.stderr.write("ERROR: %s\n" % message)
    sys.exit(1)
