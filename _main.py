from importlib import import_module
import tldextract
import validators
import os


def main():
    # ! 1- Enter website url and process it
    site_url = input('Enter a joblisting website url: ')
    # Check if entered website url is a valid domain or url name
    if not (validators.domain(site_url) or validators.url(site_url)):
        print(f'"{site_url}" is not a website url')
        return -1
    # Add 'http' in the begin of the domain name if it is forgotten
    if not site_url.startswith('http'):
        site_url = 'http://' + site_url
    # Check if the received url is in the 'joblistings' directory
    domain_name = tldextract.extract(site_url)
    joblisting_module = domain_name.domain + '_' + domain_name.suffix
    joblisting_directory = f'{os.getcwd()}/joblistings'
    if not f'{joblisting_module}.py' in os.listdir(joblisting_directory):
        print(f'"{joblisting_module}" is not in the joblisting directory')
        return -1
    # ! 2- Call the joblising website module
    module = import_module(f'joblistings.{joblisting_module}')
    result = module.extract_website(site_url)
    print(result)
    
    
# main()


################################################################################### !
################################################################################### !
##############################! TEST PURPOSE !##################################### !
################################################################################### !
################################################################################### !

from drivers.selenium_driver import call_selenium_driver
from joblistings.jobvision_ir import ExtractJob
import time
job_url = 'file:///C:/Users/AS/Desktop/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87_%D9%86%D9%88%DB%8C%D8%B3%20%D8%A7%D8%B1%D8%B4%D8%AF%20Python%20%D8%AF%D8%B1%20%D8%B4%D8%B1%DA%A9%D8%AA%20%D8%AC%D8%B1%D8%A7%D8%AD%20%DB%8C%D8%A7%D8%B1%D8%A7%D9%86%20%D9%BE%D8%A7%D8%B1%D8%B3%DB%8C%D8%A7%D9%86%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_15_2024%203_48_02%20PM).html'
driver = call_selenium_driver()
driver.get(job_url)
time.sleep(2)
ej = ExtractJob(driver=driver, job_url=job_url)
title = ej.find_job_title()
print('Job title: ', title)
company_name_link = ej.find_company_name_link()
print('Company name: ', company_name_link[0])
print('Company Link: ', company_name_link[1])
avg_salary = ej.find_offered_salary()
print('Offered average salary(million toman): ', avg_salary)
