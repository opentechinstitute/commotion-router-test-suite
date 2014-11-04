# ## installable package
# # from distutils.core import setup
import os, os.path
import sys
#
# ## pytest plugin style
# # sample ./setup.py file
# from setuptools import setup
#
# setup(
#     name="commotion-router-test-suite",
#     description="Automated test tools, primarily for testing Commotion Router's"
#                 " web user interface.",
#     author="Andrew Reynolds",
#     author_email="andrew@chambana.net",
#     url="https://github.com/opentechinstitute/commotion-router-test-suite",
#     version='0.2',
#     package_dir = {''},
#     test_suite = 'tests',
#     # long_description=read("README.md"),
#     # py_modules=['util', 'exceptions', 'browser', 'router', 'page'],
#     packages = ['objects'],
#     entry_points = {
#         'pytest11': [
#             'name_of_plugin = tests',
#         ]
#     },
#     setup_requires = [
#         'setuptools',
#         # 'python>=3',
#         ],
#     tests_require = [
#         'bunch',
#         'pytest',
#         'netifaces',
#         'selenium',
#         # 'unittest',
#         # 'random',
#     ]
# )
#
# ## pytest plugin style
# # sample ./setup.py file
# # from setuptools import setup
# #
# # setup(
# #     name="myproject",
# #     packages = ['myproject']
# #
# #     # the following makes a plugin available to pytest
# #     entry_points = {
# #         'pytest11': [
# #             'name_of_plugin = myproject.pluginmodule',
# #         ]
# #     },
# # )

try:
    if not os.path.isfile("pytest.ini"):
        raise FileNotFoundError("Pytest.ini not found. Creating file.")
except FileNotFoundError as args:
    print(args)
    try:
        import shutil
        shutil.copyfile("example-pytest.ini", "pytest.ini")
    except OSError as args:
        print("Error creating pytest.ini. ", args)
        sys.exit()
else:
    print("Don't forget to add node admin credentials to pytest.ini!")
