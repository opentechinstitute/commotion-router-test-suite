"""
Automated tests for Commotion Router based on OTI's release testing plan.

"""
import pytest

# Standard pytest command line options
PYTEST_OPTS = {
    "log_dir": None, # Usage: --logdir=/foo/bar/baz.log
    "verbose": "-v", # Options: -v or None
    "slow_tests": "--durations=5",
    "stdout": "-s",
    "testdir": "tests"
}

TESTOPTS = ' '.join ("%s" % val for val in PYTEST_OPTS.values() if val)

pytest.main(TESTOPTS)