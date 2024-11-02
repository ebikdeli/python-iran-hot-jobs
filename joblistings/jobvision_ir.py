"""Extract data for all the jobs related to the job_title from the 'jobvision.ir' and process the extracted data."""

from drivers.selenium_driver import call_selenium_driver
from save_data.save_csv import into_csv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from database import sqlite_connector
from time import sleep
import datetime
import pathlib
import os


class ExtractWebsite:
    """Extract data from jobvision.ir website."""
    def __init__(self, site_url:str, job_title:str='python') -> None:
        self.site_url = site_url
        self.job_title = job_title
        self.driver = None
    
    def start_driver(self) -> WebDriver|None:
        """Start webdriver"""
        try:
            driver = call_selenium_driver(headless=1)
        except Exception as e:
            print('Problem with selenium:\n', e.__str__())
            return None
        return driver
    
    def start(self) -> str:
        """Extract jobvision.ir jobs"""
        print(f'Call the joblisting website for the "{self.site_url}"')
        try:
            _scraped_today = False
            # Check if job links scrapped today
            if self._is_check_job_links_file_date():
                _scraped_today = True
                ##### ! For multiple line strings, we must use """ - """ format
                _continue = input(f"""'jobvision.ir' jobs scraped just today. If you want to find the jobs for 
                                  '{self.job_title}' again press 'y'. Press 'n' to exit, or press any other 
                                  key to scrap job links from the job_link file: """)
                if _continue.strip().lower() == 'n':
                    return 'Do not proceed with jobvision.ir'
            self.driver = self.start_driver()
            if not self.driver:
                return 'Exit the program for error in running selenium driver'
            # Scrap all job links for the title and write the links into a file or read job links from the file
            job_link_set = set()
            if not _scraped_today or _continue == 'y':
                page_number = 1
                # ! Get all the 'job_title' jobs in jobvision search
                job_link_set = self._get_job_links(job_link_set, page_number)
                # ! Process the every job links extracted
                print(f'Number of jobs found for "{self.job_title}" job title: {len(job_link_set)}')
                # To not repeat the above process again and save resources for a day, save the extracted job links into a file
                if not self._write_link_into_file(job_link_set):
                    self.driver.close()
                    return 'Could not enter job links into the related file'
            else:
                job_link_set = self._read_link_from_file(job_link_set)
                print(f'Number of job links found in the file is "{len(job_link_set)}"')
            # Extracted all specified data from every job page link in the 'job_link_set'
            # !!!!!!!!!!!!
            # for job_url in job_link_set:
            #     print(f'Extracting link:\n{job_url}')
            #     ej = ExtractJob(driver=self.driver, job_url=job_url)
            #     result_data = ej.start_extraction(job_describtion=False)
            #     save_result = into_csv(data=result_data, url=job_url)
            # !!!!!!!!!!!
        except Exception as e:
            print(f'CANNOT OPEN "{self.site_url}"')
            print(e.__str__())
            return 'Extraction failed'
        self.driver.close()
        return 'OK'
    
    def _get_job_links(self, job_link_set:set, page_number:int, _job_card_css_selector:str='job-card > a', _pagination_css_selector:str='.pagination-page.page-item.active') -> set:
        """Get job links in jobvision search section"""
        # ! Add job links to the job_link_set
        try:
            while True:
                print('page number: ', page_number)
                search_url = f'https://jobvision.ir/jobs/keyword/{self.job_title}?page={page_number}'
                self.driver.get(search_url)
                sleep(1)
                for jb in self.driver.find_elements(By.CSS_SELECTOR, _job_card_css_selector):
                    job_link_set.add(jb.get_attribute('href'))
                # ! Check if there are any page remain to being scraped
                try:
                    self.driver.find_element(By.CSS_SELECTOR, _pagination_css_selector)
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
    
    def _is_check_job_links_file_date(self) -> bool:
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
    
    def _write_link_into_file(self, job_link_set:set) -> bool:
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
    
    def _read_link_from_file(self, job_link_set:set) -> set:
        """Read job link urls from job_link file. If successful return True"""
        try:
            current_directory = pathlib.Path(__file__).parent.resolve()
            job_link_file_name = "_jobvision_links.txt"
            with open(f'{os.path.join(current_directory, job_link_file_name)}', 'rt') as f:
                data = f.readlines()
            for d in data:
                if d.startswith('http'):
                    job_link_set.add(d.strip().replace('\n', ''))
            print('Successfully read job urls from the file')
        except Exception as e:
            print('A problem happend:\n', e.__str__())
        return job_link_set


class ExtractJob:
    """In job page, extract all data from a single_page page."""
    def __init__(self, driver: WebDriver, job_url: str) -> None:
        self.driver = driver
        self.job_url = job_url
        
    def start_extraction(self, title:bool=True, company_name:bool=True, company_link:bool=True,
                        salary:bool=True, experience:bool=True, age:bool=True, education:bool=True,
                        skills:bool=True, gender:bool=True, language:bool=True, description:bool=True) -> dict:
        """Start extracting data from a job page in jobvision. Return result as a dict"""
        _result = {'title': None, 'company_name': None, 'company_link': None, 'salary': None, 'experience': None,
                   'age': None, 'education': None, 'skills': None, 'gender': None, 'language': None, 'description': None}
        if title:
            _result.update({'title': self.find_job_title()})
        company_name, company_link = self.find_company_name_link()
        if company_name:
            _result.update({'company_name': company_name})
        if company_link:
            _result.update({'company_link': company_link})
        if salary:
            _result.update({'salary': self.find_offered_salary()})
        if experience:
            _result.update({'experience': self.find_experience_needed()})
        if age:
            _result.update({'age': self.find_age_suggestion()})
        if education:
            _result.update({'education': self.find_education()})
        if skills:
            _result.update({'skills': self.find_skills_needed()})
        if gender:
            _result.update({'gender': self.find_gender()})
        if language:
            _result.update({'language': self.find_language()})
        if description:
            _result.update({'description': self.find_job_describe()})
        return _result
    
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
    
    def find_offered_salary(self, salary_selector:str='.job-detail-external-card .yn_price') -> list[int, int]:
        """Find offered job salary monthly in millions of Toman. Return 2-element list of [min-salary, max-salary].
        If no specific salary found return [0, 0]. If only an specific salary found set both min_salary and max_salary the same"""
        min_salary, max_salary = 0, 0
        try:
            _found_salary = self.driver.find_element(By.CSS_SELECTOR, salary_selector).text
            if _found_salary:
                _salary_list = list()
                for _ in _found_salary.split():
                    if _.strip().isdigit():
                        _salary_list.append(int(_.strip()))
                if _salary_list:
                    min_salary, max_salary = min(_salary_list), max(_salary_list)
                    return [min_salary, max_salary]
        except Exception as e:
            print(f'Alert: Could not find "salary offered":\n{e.__str__()}')
        return [min_salary, max_salary]
    
    def find_experience_needed(self, experience_selector:str='.job-specification .col.mr-2.px-0.word-break') -> int:
        """Find experience needed for the job. Return int as years. If no experience found or mentioned return 0"""
        exp = 0
        try:
            exp_text = self.driver.find_element(By.CSS_SELECTOR, experience_selector).text.strip()
            if 'سال' in exp_text or 'years' in exp_text:
                for _ in exp_text.split():
                    if _.strip().isdigit():
                        exp = int(_.strip())
        except Exception:
            try:
                experience_selector = '.job-specification .col.ml-2.px-0.word-break'
                exp_text = self.driver.find_element(By.CSS_SELECTOR, experience_selector).text.strip()
                if 'سال' in exp_text or 'years' in exp_text:
                    for _ in exp_text.split():
                        if _.strip().isdigit():
                            exp = int(_.strip())
            except Exception as e:
                print(f'Alert: Could not find "experience":\n{e.__str__()}')
        return exp
    
    def find_age_suggestion(self, age_suggestion_selector:str='.job-specification .requirement-value.text-black.bg-light.py-2.px-3.ng-star-inserted') -> list[int, int]:
        """Find the applican age suggestion for the job. Return 2-element list as [min_age, max_age]. If no age suggestion found return [0, 0]"""
        min_age, max_age = 0, 0
        try:
            _found_age = self.driver.find_element(By.CSS_SELECTOR, age_suggestion_selector).text
            if _found_age:
                _age_list = list()
                for _ in _found_age.split():
                    if _.strip().isdigit():
                        _age_list.append(int(_.strip()))
                if _age_list:
                    min_age, max_age = min(_age_list), max(_age_list)
                    return [min_age, max_age]
        except Exception as e:
            print(f'Alert: Could not find "age suggestion":\n{e.__str__()}')
        return [min_age, max_age]
    
    def find_gender(self, gender_selector:str='.job-specification .requirement-value.text-black.bg-light.py-2.px-3') -> str:
        """Find applicant gender. Return gender. If gender not found return empty string"""
        gender = str()
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, gender_selector)
            for e in elements:
                if ('زن' in e.text.strip().lower() or 'women' in e.text.strip().lower()) and not ('مرد' in e.text.strip().lower() or 'men' in e.text.strip().lower()):
                    gender = 'F'
                elif  ('مرد' in e.text.strip().lower() or 'men' in e.text.strip().lower()) and not ('زن' in e.text.strip().lower() or 'women' in e.text.strip().lower()):
                    gender = 'M'
        except Exception as e:
            print(f'Alert: Could not find "gender": {e.__str__()}')
        return gender
    
    def find_language(self, language_selector:str='.job-specification .requirement-value.bg-light.py-2.px-3') -> str:
        """Find language needed for the job. Return string. If no language found return empty string"""
        lang = str()
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, language_selector)
            for e in elements:
                if 'english' in e.text.strip().lower() or 'انگلیسی' in e.text.strip():
                    lang = 'English'
                elif 'arabi' in e.text.strip().lower() or 'عربی' in e.text.strip():
                    lang = 'Arabic'
                elif 'german' in e.text.strip().lower() or 'المانی' in e.text.strip() or 'آلمانی' in e.text.strip():
                    lang = 'German'
                elif 'fr' in e.text.strip().lower() or 'فرانس' in e.text.strip():
                    lang = 'French'
                elif 'tu' in e.text.strip().lower() or 'ترک' in e.text.strip():
                    lang = 'Turkish'
        except Exception as e:
            print(f'Alert: Could not found "language": {e.__str__()}')
        return lang
    
    def find_skills_needed(self, skills_selector:str='.row.col-11.px-0 div') -> list[str]:
        """Find needed skills"""
        skills_list = list()
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, skills_selector)
            for e in elements:
                skills_list.append(e.text.replace('-', ':'))
        except Exception as e:
            print(f'Alert: Could not find the "skills": {e.__str__()}')
        return skills_list
    
    def find_education(self, education_selector:str='.job-specification .col-12.col-lg-9.px-lg-0 .tag.row.text-white.bg-secondary.rounded-sm.py-1.px-2.ml-2') -> list[str]:
        """Find education needed for the job. Return education as list. If education not found or not suggested return empty list."""
        education = list()
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, education_selector)
            for e in elements:
                if 'کارشناس' in e.text.strip() or 'کاردانی' in e.text.strip() or 'Bachelor' in e.text.split():
                    education.append(e.text.strip().replace('\n', ' ').replace('|', ':'))
        except Exception as e:
            print(f'Alert: Could not find the "education": {e.__str__()}')
        return education
    
    def find_job_describe(self, job_describe_selector:str='.col-12.row.text-black.px-0.mb-3') -> str:
        """Find job description. Return it as string. If not found return empty string"""
        job_describe = str()
        try:
            job_describe = self.driver.find_element(By.CSS_SELECTOR, job_describe_selector).text.strip()
        except Exception as e:
            print(f'Alert: Could not find "job descrition": {job_describe}')
        return job_describe


class ProcessExtractedJobData:
    """Process the job data extracted from jobvision website. 'data' is a dictionary contains all the data extracted in ExtractJob
    start_extraction"""
    def __init__(self, data:dict):
        self.data = data

    def education(self) -> list[list[str, str]]:
        """Process the education data extracted from 'jobvision.ir' website and insert the data into 'education' table.\n
        If successful returns list of lists. Each inner list is a 2-element string. First element is degree and the
        second element is the course. For eg:.\n
        [['Bachelor', 'Computer], ['Bachelor': 'Accounting']]\n
        If no education found return empty list."""
        try:
            education_list_processed = list()
            _education_list: list[str]|None = self.data.get('education', None)
            if not _education_list:
                print('No education found for the job...')
            # Process each job separately. 'education_list' is like this:
            # ['Bachelor : Computer and IT' , 'Bachelor : Electrical Engineering' , 'Bachelor : Finance/Accounting']
            for _education_str in _education_list:
                degree, course = _education_str.split(':')
                degree = degree.strip()
                course = course.strip()
                # ! Check if there are more than one education is in the 'course' separated by '/' (For now we ignore separation)
                # !!!!!!!!!!!!!    MORE PROCESS HERE IF NEEDED    !!!!!!!!!!!!!!!!!
                education_list_processed.append([degree, course])
        except Exception as e:
            print('Error in joblistings.jobvision.ProcessExtractedJobData.education:\n', e.__str__())
        return education_list_processed
    
    def skill(self) -> list[list[str, str]]:
        """Process the skill data extracted from 'jobvision.ir' website and insert the data into 'skill' table.\n
        If successful returns list of lists. Each inner list is a 2-element string. First element is skill_name and the
        second element is the skill_level. For eg:.\n
        [['Python', 'Intermediate], ['Linux': 'Advanced']]\n
        If no skill found return empty list."""
        try:
            skill_list_processed = list()
            _skill_list: list[str]|None = self.data.get('skill', None)
            if not _skill_list:
                print('No skill found for the job...')
            # Process each job separately. 'skill_list' is like this:
            # ['Java : Advanced' , 'Ruby on Rails : Intermediate' , 'Python : Advanced' , 'ASP.Net : Advanced' , 'JavaScript : Intermediate' , 'Go : Intermediate' , 'PHP : Intermediate' , 'Node.js : Intermediate' , 'Laravel : Advanced' , '.Net Core / .Net : Advanced']
            for _skill_str in _skill_list:
                skill_name, skill_level = _skill_str.split(':')
                skill_name = skill_name.strip()
                skill_level = skill_level.strip()
                # !!!!!!!!!!!!!    MORE PROCESS HERE IF NEEDED    !!!!!!!!!!!!!!!!!
                skill_list_processed.append([skill_name, skill_level])
        except Exception as e:
            print('Error in joblistings.jobvision.ProcessExtractedJobData.skill:\n', e.__str__())
        return skill_list_processed
    
    def description(self) -> object:
        pass
