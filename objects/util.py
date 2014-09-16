"""Common utilities for the commotion router tests"""
import sys


def error(message):
    """Basic error reporting function"""
    sys.stderr.write("ERROR: %s\n" % message)
    sys.exit(1)
