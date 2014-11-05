"""
Config instructions and test fixtures
"""

import pytest
import os
import sys


# # these are just some fun dividiers to make the output pretty
# # completely unnecessary, I was just playing with autouse fixtures
# @pytest.fixture(scope="function", autouse=True)
# def divider_function(request):
#     print('\n        --- function %s() start ---' % request.function.__name__)
#     def fin():
#             print('        --- function %s() done ---' % request.function.__name__)
#     request.addfinalizer(fin)


@pytest.fixture(scope="session", autouse=True)
def set_up_ini(request):
    print("in set_up_ini")
    try:
        # need to back up a directory
        path = os.path.dirname(os.path.abspath("conftest.py"))
        print(path)
        if not os.path.isfile(path + "/pytest.ini"):
            raise FileNotFoundError("Pytest.ini not found.")
    except FileNotFoundError as args:
        print(args)
        try:
            import shutil
            print("Creating pytest.ini")
            shutil.copyfile(path + "/example-pytest.ini", path + "/pytest.ini")
        except OSError as args:
            print("Error creating pytest.ini. ", args)
    else:
        print("Don't forget to add node admin credentials to pytest.ini!")
