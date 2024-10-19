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
    try:
        module = import_module(f'joblistings.{joblisting_module}')
        ew = module.ExtractWebsite(site_url)
        result = ew.start()
        print(result)
    except Exception as e:
        print(f'Error: Cannot extract data from "{joblisting_module}"')

main()


################################################################################### !
################################################################################### !
##############################! TEST PURPOSE !##################################### !
################################################################################### !
################################################################################### !

# from drivers.selenium_driver import call_selenium_driver
# from joblistings.jobvision_ir import ExtractJob
# import time
# job_url = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87_%D9%86%D9%88%DB%8C%D8%B3%20%D8%A7%D8%B1%D8%B4%D8%AF%20Python%20%D8%AF%D8%B1%20%D8%B4%D8%B1%DA%A9%D8%AA%20%D8%AC%D8%B1%D8%A7%D8%AD%20%DB%8C%D8%A7%D8%B1%D8%A7%D9%86%20%D9%BE%D8%A7%D8%B1%D8%B3%DB%8C%D8%A7%D9%86%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_15_2024%203_48_02%20PM).html'
# job_url = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20Data%20Scientist%20%D8%AF%D8%B1%20%D8%B4%D8%A7%D9%BE%DB%8C%D9%86%D9%88%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_19_2024%2012_24_29%20PM).html'
# job_url = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20Full%20Stack%20Software%20Engineer%20(AI%20Developer)%20%D8%AF%D8%B1%20%D9%85%D9%88%D8%B3%D8%B3%D9%87%20%D9%85%D9%87%D8%A7%D8%AC%D8%B1%D8%AA%DB%8C%20applyland%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_19_2024%2012_24_35%20PM).html'
# driver = call_selenium_driver(headless=1)
# driver.get(job_url)
# time.sleep(2)
# ej = ExtractJob(driver=driver, job_url=job_url)
# res = ej.start_extraction(job_describtion=False)
# print(res)
