commotion-router-test-suite
===========================

VERY EARLY DRAFT

Automated tests for 
[Commotion Router](https://github.com/opentechinstitute/commotion-router/)

Originally designed to minimize manual input testing on router UI.  Many tests,
particularly tests of unprivileged functions, use Selenium where it is very
inefficient to do so, but are included as simple examples of test structure.

Basic Structure
_______________

Tests

+ commotiontestobjects/ - Objects representing the user
++ browserobjects
++ util
++ commotionrouterobjects/ - Objects representing router nodes
+++ routerobjects - router-specific node objects
+++ pageobjects/ - Objects found only in router-based UI pages
++++ crpageobjects - Functions to build UI page models from component elements

Resources
_________

* http://engineeringquality.blogspot.com/2012/12/python-quick-and-dirty-pageobject.html
* http://pragprog.com/magazines/2010-08/page-objects-in-python
* http://computerrecipes.wordpress.com/2012/09/11/page-objects-design-pattern-for-selenium-webdriver/
