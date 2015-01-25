"""Custom exceptions for the Commotion Router Test Suite"""

import requests

class CommotionIPError(ConnectionError):
    """
    Raised when the test host does not have a valid Commotion IP address.
    Subclass of the built-in ConnectionError base class.
    """
    def __init__(self, value):
        self.msg = "Connect to a Commotion AP before running tests: "
        self.value = value
    def __str__(self):
        string = self.msg + repr(self.value)
        return string
