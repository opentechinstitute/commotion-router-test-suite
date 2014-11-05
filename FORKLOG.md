Fork Changelog
==============

areynold/master differs from oti/master in the following ways:
+ merge pytest-config branch to master (https://github.com/opentechinstitute/commotion-router-test-suite/pull/7)
+ merge python3 branch to master (https://github.com/opentechinstitute/commotion-router-test-suite/pull/9)
+ create admin-profile branch
+ create ap-exception branch
+ merge ap-exception to admin-profile
+ merge admin-profile to master
+ create ignore branch
+ merge ignore branch to master

Admin-Profile Summary
_____________________

Task: Create a browser profile or test suite config file allowing
testers to save node details such as the router password.
The solution should allow both successful login and, where
login testing is not necessary, direct (or transparent) access 
to the node admin pages.

Implemented as an additional configparser section in the existing
pytest.ini file. Could also be implemented as a constant in config.py,
then imported as needed, but it seemed beneficial to keep all test
config options in a single file.

Pytest uses a session-scoped, autouse fixture (defined in tests/conftest.py)
to check for pytest.ini. If no file is found, a clean copy will be created
using an example file.

Tests using the admin credentials should test for the default password
(ChangeMe), and use pytest.mark.xfail to trigger an expected failure
until the default password is changed.

To test:
1. Connect to a Commotion node.
2. Run `py.test tests/test_commotion_router_admin.py`. 
The test_login_succeed test should return an expected failure (pytest xfail).
3. Open pytest.ini and change admin_password to the correct node password.
4. Rerun `py.test tests/test_commotion_router_admin.py`. test_login_succeed
should pass. test_login_fail should also pass (meaning bad values are
rejected).
5. Run `git status` in the project root. Pytest.ini should not be listed
 as a modified file.


AP Exception Summary
____________________

Adds a custom exception to accurately identify a test host that
has not been connected to a Commotion access point. Closes 
https://github.com/opentechinstitute/commotion-router-test-suite/issues/8

To test the AP exception:
1. Run py.test while not connected to a Commotion node. Execution should fail,
and your traceback should include instructions to connect to a Commotion AP
before running the tests.
