from importlib import import_module
import tldextract
import os
import time


def main():
    # ! 1- Enter website url and process it
    website_codes = {'1': 'jobvision.ir'}
    while True:
        enter_number = input('Website codes to scrap: Press "1" for "jobvision.ir". To quit press "n": ')
        if enter_number.strip().lower() == 'n':
            print('Program terminated...')
            exit()
        elif enter_number.strip() not in website_codes.keys():
            print("Please enter a correct number\n")
        else:
            print(f'"{website_codes[enter_number]}" will be scrapped...')
            break
    site_url = 'http://' + website_codes[enter_number]
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

# main()
# exit()
################################################################################### !
################################################################################### !
##############################! TEST PURPOSE !##################################### !
################################################################################### !
################################################################################### !

from database.sqlite_connector import SqlliteConnection
import sqlite3
from sqlite3 import Connection, Cursor
sc: SqlliteConnection = SqlliteConnection()
# sc.get_or_create_extracted_data()
sc.close_connect()
exit()


from drivers.selenium_driver import call_selenium_driver
from joblistings.jobvision_ir import ExtractJob
import time
from save_data.save_csv import into_csv
job_url = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87_%D9%86%D9%88%DB%8C%D8%B3%20%D8%A7%D8%B1%D8%B4%D8%AF%20Python%20%D8%AF%D8%B1%20%D8%B4%D8%B1%DA%A9%D8%AA%20%D8%AC%D8%B1%D8%A7%D8%AD%20%DB%8C%D8%A7%D8%B1%D8%A7%D9%86%20%D9%BE%D8%A7%D8%B1%D8%B3%DB%8C%D8%A7%D9%86%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_15_2024%203_48_02%20PM).html'
# job_url = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20Data%20Scientist%20%D8%AF%D8%B1%20%D8%B4%D8%A7%D9%BE%DB%8C%D9%86%D9%88%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_19_2024%2012_24_29%20PM).html'
# job_url = 'file:///C:/CODES/PYTHON/python-iran-hot-jobs/_resources/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%20Full%20Stack%20Software%20Engineer%20(AI%20Developer)%20%D8%AF%D8%B1%20%D9%85%D9%88%D8%B3%D8%B3%D9%87%20%D9%85%D9%87%D8%A7%D8%AC%D8%B1%D8%AA%DB%8C%20applyland%20_%20%D8%AC%D8%A7%D8%A8_%D9%88%DB%8C%DA%98%D9%86%20(10_19_2024%2012_24_35%20PM).html'
driver = call_selenium_driver(headless=1)
driver.get(job_url)
time.sleep(2)
ej = ExtractJob(driver=driver, job_url=job_url)
res = ej.start_extraction(job_description=False)
print(res)
into_csv(res, job_url)
