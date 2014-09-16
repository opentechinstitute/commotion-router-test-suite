Fork Changelog
==============

areynold/master differs from oti/master in the following ways:
+ merge pytest-config branch to master
+ merge python3 branch to master
+ create admin-profile branch
+ create ap-exception branch

Admin-Profile Summary
_____________________

Create a browser profile or test suite config file allowing
testers to save node details such as the router password.
The solution should allow both successful login and, where
login testing is not necessary, direct (or transparent) access 
to the node admin pages.

AP Exception Summary
____________________

Adds a custom exception to accurately identify a test host that
has not been connected to a Commotion access point. Closes 
https://github.com/opentechinstitute/commotion-router-test-suite/issues/8
