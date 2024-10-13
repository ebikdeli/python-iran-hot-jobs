from drivers.selenium_driver import call_selenium_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import datetime
import pathlib
import os


def extract_website(site_url: str, job_title: str='python') -> str:
    """Extract jobvision.ir jobs"""
    print(f'Call the joblisting website for the "{site_url}"')
    try:
        if _is_check_job_links_file_date():
            print('Just today jobvision jobs scraped')
            return 'No need to scrapp jobvision'
        driver = call_selenium_driver(headless=1)
        job_link_set = set()
        page_number = 1
        # ! Get all the 'python' jobs
        job_link_set = _get_job_links(driver, job_title, job_link_set, page_number)
        # ! To not repeat the above process again save the extracted job links into a file
        # ! Process every 'job_cards' received
        print(f'Number of jobs found for "{job_title}" job title: {len(job_link_set)}')
    except Exception as e:
        print(f'CANNOT OPEN "{site_url}"')
        print(e.__str__())
        # return -1
    driver.close()
    return 'OK'


def _get_job_links(driver:WebDriver, job_title:str, job_link_set:set, page_number:int, _job_card_css_selector:str='job-card > a', _pagination_css_selector:str='.pagination-page.page-item.active') -> set:
    """Helper function to get job links in jobvision search section"""
    # ! Add job links to the job_link_set
    try:
        while True:
            print('page number: ', page_number)
            search_url = f'https://jobvision.ir/jobs/keyword/{job_title}?page={page_number}'
            driver.get(search_url)
            sleep(1)
            for jb in driver.find_elements(By.CSS_SELECTOR, _job_card_css_selector):
                job_link_set.add(jb.get_attribute('href'))
            # ! Check if there are any page remain to being scraped
            try:
                driver.find_element(By.CSS_SELECTOR, _pagination_css_selector)
                page_number += 1
            except NoSuchElementException:
                print(f'No element found as "{_pagination_css_selector}" or no page remains')
                return job_link_set
            except Exception as e:
                print(e.__str__())
                return job_link_set
    except Exception as e:
        print(f'Problem in scraping below url:\n{search_url}\nError:\n{e.__str__()}')
        return job_link_set


def _is_check_job_links_file_date() -> bool:
    """Check the date in the first line of the '_jobvision_links.txt'. If less than a day passed since the job scrapped, return True. If no file found, create a new file"""
    cd = pathlib.Path(__file__).parent.resolve()
    try:
        with open(f'{os.path.join(cd, "_jobvision_links.txt")}', 'rt') as f:
            date_str = f.readline()
        date_obj = datetime.date.fromisoformat(date_str)
        td = datetime.date.today() - date_obj
        if not td.days:
            return True
    # If the file does not exist create it and enter today date in the first line in the file
    except FileNotFoundError:
        with open(f'{os.path.join(cd, "_jobvision_links.txt")}', 'wt') as f:
            f.write(datetime.date.today().strftime('%Y-%m-%d'))
        print('Jobvision job list file just created')
    return False
