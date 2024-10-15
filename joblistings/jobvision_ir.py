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
        # ! Get all the 'job_title' jobs in jobvision search
        job_link_set = _get_job_links(driver, job_title, job_link_set, page_number)
        # ! Process the every job links extracted
        print(f'Number of jobs found for "{job_title}" job title: {len(job_link_set)}')
        # To not repeat the above process again and save resources for a day, save the extracted job links into a file
        if not _write_link_into_file(job_link_set):
            driver.close()
            return 'Could not enter job links into related file'
        # Extracted all specified data from every job page link in the 'job_link_set'
        # !!!!!!!!!!!!
        # for job_url in job_link_set:
        #     print(f'Extracting link:\n{job_url}')
        #     ej = ExtractJob(driver=driver, job_url=job_url)
        #     title = ej.find_job_title()
        #     company_name, company_link = ej.find_company_name_link()
        # !!!!!!!!!!!
    except Exception as e:
        print(f'CANNOT OPEN "{site_url}"')
        print(e.__str__())
        # return -1
    driver.close()
    return 'OK'


def _get_job_links(driver:WebDriver, job_title:str, job_link_set:set, page_number:int, _job_card_css_selector:str='job-card > a', _pagination_css_selector:str='.pagination-page.page-item.active') -> set:
    """Get job links in jobvision search section"""
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
    current_directory = pathlib.Path(__file__).parent.resolve()
    job_link_file_name = "_jobvision_links.txt"
    try:
        with open(f'{os.path.join(current_directory, job_link_file_name)}', 'rt') as f:
            link_sample = f.readlines(400)
            date_str = link_sample[0]
        date_obj = datetime.date.fromisoformat(date_str.replace('\n', ''))
        td = datetime.date.today() - date_obj
        if td.days == 0 and len(link_sample) > 2:
            return True
    # If the file does not exist create it and enter today date in the first line in the file
    except Exception:
        with open(f'{os.path.join(current_directory, job_link_file_name)}', 'wt') as f:
            f.write(datetime.date.today().strftime('%Y-%m-%d'))
        print('Jobvision job list file just created')
    return False


def _write_link_into_file(job_link_set:set) -> bool:
    """Write job link urls into job_link file. If successful return True"""
    try:
        current_directory = pathlib.Path(__file__).parent.resolve()
        job_link_file_name = "_jobvision_links.txt"
        with open(f'{os.path.join(current_directory, job_link_file_name)}', 'wt') as f:
            f.write(datetime.date.today().strftime('%Y-%m-%d'))
            for ul in job_link_set:
                f.write(f"{'\n\n' + ul}")
        print('Successfully entered job urls into file')
        return True
    except Exception as e:
        print('A problem happend:\n', e.__str__())
        return False


class ExtractJob:
    """In job page, extract all data from the page"""
    def __init__(self, driver: WebDriver, job_url: str):
        self.driver = driver
        self.job_url = job_url

    def extract(self) -> object:
        """Extract data from a job page in jobvision"""
        pass
    
    def find_job_title(self, title_selector:str='h1') -> str:
        """Find job title. Return job title as str"""
        # job_title_css_selector="h1"
        title = str()
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, title_selector).text
        except Exception as e:
            print(f'Alert: Could not find the "job title":\n{e.__str__()}')
        return title
    
    def find_company_name_link(self, company_selector:str='.job-detail-external-card a') -> list[str, str]:
        """Find company name and company link. Return a list of [comapny_name , company_link]"""
        # company_name_css_selector=".job-detail-external-card"
        company_name_link = list()
        try:
            company_name_link.append(self.driver.find_element(By.CSS_SELECTOR, company_selector).text)
            # Save company link for future use
            company_name_link.append(self.driver.find_element(By.CSS_SELECTOR, company_selector).get_attribute('href'))
        except Exception as e:
            print(f'Alert: Could not find the "company name" and "company link:\n{e.__str__()}')
        return company_name_link
    
    def find_offered_salary(self, salary_selector:str='.job-detail-external-card .yn_price') -> int:
        """Find offered [average] job salary monthly because in some jobs instead of a specific amount, there is a range for salary.
        Return an integer as average salary in million toman. 0 means no amount offered"""
        avg_salary_offered = 0
        try:
            _found_salary = self.driver.find_element(By.CSS_SELECTOR, salary_selector).text
            if _found_salary:
                _salary_list = list()
                for fs in _found_salary.split():
                    if fs.isdigit():
                        _salary_list.append(int(fs))
                avg_salary_offered = int(sum(_salary_list) / len(_salary_list)) if len(_salary_list) > 1 else _salary_list[0]
        except Exception as e:
            print(f'Alert: Could not find "salary offered":\n{e.__str__()}')
        return avg_salary_offered
