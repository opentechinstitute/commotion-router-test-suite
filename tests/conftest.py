"""
Config instructions and test fixtures
"""

import pytest
import os


@pytest.fixture(scope="session", autouse=True)
def setup_ini(request):
    print("in set_up_ini")
    try:
        # need to back up a directory
        path = os.path.dirname(os.path.abspath("conftest.py"))
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

    # # Necessary?
    # def finalize_setup_ini():
    #     return None
    #     request.addfinalizer(finalize_setup_ini)
