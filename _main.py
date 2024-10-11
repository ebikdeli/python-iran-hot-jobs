from drivers.selenium_driver import call_selenium_driver
from time import sleep
import importlib


def main():
    site_url = input('Enter a joblisting website url: ')
    try:
        driver = call_selenium_driver()
        driver.get(site_url)
    except Exception as e:
        print(f'CANNOT OPEN "{site_url}"')
        exit()
    