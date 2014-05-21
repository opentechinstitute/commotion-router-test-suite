"""
Automated tests for Commotion Router based on OTI's release testing plan.

"""
import unittest
import importlib
import time
import sys
import os
import logging
# faulthandler is a python3 module
#import faulthandler

def create_runner(verbosity_level=None):
    """creates a testing runner.

    suite_type: (string) suites to run [acceptable values = suite_types in build_suite()]
    """
    #faulthandler.enable()
    logging.basicConfig(filename='./logs/test_commotion_router_ui.log',
                        level=logging.INFO)
    logging.warning("Specify path to log directory")
    loader = unittest.TestLoader()
    tests = loader.discover('.', '*_tests.py')
    testRunner = unittest.runner.TextTestRunner(verbosity=verbosity_level, warnings="always")
    testRunner.run(tests)



if __name__ == '__main__':
    """Creates argument parser for required arguments and calls test runner"""
    import argparse
    parser = argparse.ArgumentParser(description='Commotion Router test suite')
    parser.add_argument("-v", "--verbosity", nargs="?", default=2, const=2, dest="verbosity_level", metavar="VERBOSITY", help="make test_suite verbose")

    args = parser.parse_args()
    create_runner(args.verbosity_level)

