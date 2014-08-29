[![alt tag](http://img.shields.io/badge/maintainer-critzo-orange.svg)](https://github.com/critzo)
commotion-router-test-suite
===========================

VERY EARLY DRAFT

Automated tests for 
[Commotion Router](https://github.com/opentechinstitute/commotion-router/)

Originally designed to minimize manual input testing on router UI.  Many tests,
particularly tests of unprivileged functions, use Selenium where it is very
inefficient to do so, but are included as simple examples of test structure.


Usage
_____

`py.test` to run all available tests, or 
`py.test tests/test_commotion_router_admin.py` to run a specific set of tests

Pytest will automatically discover any tests using its defined naming conventions.

Pytest command line defaults are set in the file pytest.ini.
Pytest behavior can be configured using the file tests/conftest.py.

See the [Pytest documentation](http://pytest.org/latest/) for details.


Required Packages
_________________

+ Python (v3)
+ Python development libraries
+ Bunch
+ Pytest
+ Netifaces
+ Selenium
+ Unittest
+ Logging
+ Random


Basic Structure
_______________

+ tests/ - Unit tests, separated by type or profile
+ objects/ - All objects used in the tests
  + browser.py - Objects representing the browser/user
  + malicious_strings.py - Standard strings for use in input validation tests
  + util.py - Utility functions
  + router/ - Objects used in router-based tests
    + router.py - router-specific node objects
    + page/ - Objects found only in router-based UI pages
      + page.py - Page definitions for router-based nodes


Resources
_________

* http://pytest.org/latest/example/
* http://pytest.org/latest/contents.html
* http://engineeringquality.blogspot.com/2012/12/python-quick-and-dirty-pageobject.html
* http://pragprog.com/magazines/2010-08/page-objects-in-python
* http://computerrecipes.wordpress.com/2012/09/11/page-objects-design-pattern-for-selenium-webdriver/
