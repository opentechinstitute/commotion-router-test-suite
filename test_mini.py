from selenium import webdriver
import configparser

config = configparser.ConfigParser()
config.read('pytest.ini')
password = config.get('admin_common', 'admin_password')

ff_admin = webdriver.FirefoxProfile()
print("ff_admin: ", dir(ff_admin), "\n")
print("default_preferences: ", ff_admin.default_preferences, "\n")
print("userPrefs: ", ff_admin.userPrefs, "\n")

print(password)