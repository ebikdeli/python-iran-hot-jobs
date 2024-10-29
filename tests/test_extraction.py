from drivers.selenium_driver import call_selenium_driver
from joblistings.jobvision_ir import ExtractJob
from save_data.save_csv import into_csv
from selenium.webdriver.chrome.webdriver import WebDriver
import time
import unittest


class TestSeleniumDriver(unittest.TestCase):
    def test_selenium_driver(self):
        driver: WebDriver = call_selenium_driver(headless=1)
        self.assertEqual(isinstance(driver, WebDriver), True)


class TestJobvisionExtraction(unittest.TestCase):
    def setUp(self):
        self.job_url_1 :str = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87_%D9%86%D9%88%DB%8C%D8%B3%20%D8%A7%D8%B1%D8%B4%D8%AF%20Python%20%D8%AF%D8%B1%20%D8%B4%D8%B1%DA%A9%D8%AA%20%D8%AC%D8%B1%D8%A7%D8%AD%20%DB%8C%D8%A7%D8%B1%D8%A7%D9%86%20%D9%BE%D8%A7%D8%B1%D8%B3%DB%8C%D8%A7%D9%86%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_15_2024%203_48_02%20PM).html'
        self.job_url_2 :str = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20Data%20Scientist%20%D8%AF%D8%B1%20%D8%B4%D8%A7%D9%BE%DB%8C%D9%86%D9%88%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_19_2024%2012_24_29%20PM).html'
        self.job_url_3 :str = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20Full%20Stack%20Software%20Engineer%20(AI%20Developer)%20%D8%AF%D8%B1%20%D9%85%D9%88%D8%B3%D8%B3%D9%87%20%D9%85%D9%87%D8%A7%D8%AC%D8%B1%D8%AA%DB%8C%20applyland%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_19_2024%2012_24_35%20PM).html'
        self.driver: WebDriver = call_selenium_driver(headless=1)
    
    def test_extract_job_url_1(self):
        self.driver.get(self.job_url_1)
        time.sleep(2)
        ej = ExtractJob(driver=self.driver, job_url=self.job_url_1)
        res = ej.start_extraction(job_description=False)
        print(res)
        # into_csv(res, job_url)
        
    def test_extract_job_url_2(self):
        self.driver.get(self.job_url_2)
        time.sleep(2)
        ej = ExtractJob(driver=self.driver, job_url=self.job_url_2)
        res = ej.start_extraction(job_description=False)
        print(res)
        # into_csv(res, job_url)
        
    def test_extract_job_url_3(self):
        self.driver.get(self.job_url_3)
        time.sleep(2)
        ej = ExtractJob(driver=self.driver, job_url=self.job_url_3)
        res = ej.start_extraction(job_description=False)
        print(res)
        # into_csv(res, job_url)
