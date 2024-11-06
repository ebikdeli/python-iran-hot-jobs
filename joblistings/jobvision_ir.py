"""Extract data for all the jobs related to the job_title from the 'jobvision.ir' and process the extracted data."""

from drivers.selenium_driver import call_selenium_driver
from save_data.save_csv import into_csv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from database.sqlite_connector import SqliteConnection
from . import _equivalence
from time import sleep
import datetime
import pathlib
import os



class ExtractWebsite:
    """Extract data from jobvision.ir website."""
    def __init__(self, site_url:str, job_title:str='python', single_link:str='', sql_db='sqlite') -> None:
        self.site_url = site_url
        self.job_title = job_title
        self.single_link = single_link
        self.driver = None
        self.sql_db = sql_db
    
    
    def start(self) -> str:
        """Extract jobvision.ir jobs"""
        print(f'Call the joblisting website for the "{self.site_url}"\n')
        try:
            # Start chrome driver
            self.driver = self._start_driver()
            if not self.driver:
                return 'Exit the program for error in running selenium driver'
            # Start database connector
            if self.sql_db == 'sqlite':
                db_connector = SqliteConnection()
            
            # Check if there is a job link in 'self.single_link' just scrap the link and ignore all the links in the website
            if not self.single_link:
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
                    
                # Scrap all job links for the title and write the links into a file or read job links from the file
                job_link_set = set()
                if not _scraped_today or _continue == 'y':
                    page_number = 1
                    # ! Get all the 'job_title' jobs in jobvision search
                    job_link_set = self._get_job_links(job_link_set, page_number)
                    # ! Process the every job links extracted
                    print(f'Number of jobs found for "{self.job_title}" job title: {len(job_link_set)}\n')
                    # To not repeat the above process again and save resources for a day, save the extracted job links into a file
                    if not self._write_link_into_file(job_link_set):
                        self.driver.close()
                        return 'Could not enter job links into the related file'
                else:
                    job_link_set = self._read_link_from_file(job_link_set)
                    print(f'Number of job links found in the file is "{len(job_link_set)}"\n')
                    
            # Add the single_link to the 'job_link_set' to just scrap that page
            else:
                job_link_set = set()
                job_link_set.add(self.single_link)
                
            # Extracted all specified data from every job page link in the 'job_link_set'
            # !!!!!!!!!!!!
            for job_url in job_link_set:
                # Check if 'job_url' is already in the database 
                if db_connector.check_job_url(job_url=job_url):
                    print('Job link:\n', job_url, '\n', 'is already in the jobs table...\n')
                    continue
                print(f'Extract job link:\n"{job_url}"\n')
                # Load the 'job_url' with 'driver'
                self.driver.get(job_url)
                # Extract the job and scrap all needed data from the job url
                erj = ExtractRawJob(driver=self.driver, job_url=job_url)
                raw_data = erj.start_extraction(description=False)
                # Insert data into the database
                normalized_data = normalize_data_for_db(raw_data)
                result = insert_data_into_sqlite(db_connector, normalized_data)
            # !!!!!!!!!!!
            
        except Exception as e:
            print(f'Error in "joblistings.jobvision_ir.ExtractWebsite.start":\n{e.__str__()}\n')
            return 'failed'
        
        # Close connection
        db_connector.close_connect()
        # Close driver
        self.driver.close()
        return 'OK'
    
    
    def _start_driver(self) -> WebDriver|None:
        """Start webdriver"""
        try:
            self.driver = call_selenium_driver(headless=1)
        except Exception as e:
            print('Problem with selenium:\n', e.__str__(), '\n')
            return None
        return self.driver
    
    
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
                    print(f'No element found as "{_pagination_css_selector}" or no page remains\n')
                    return job_link_set
                except Exception as e:
                    print(e.__str__(), '\n')
                    return job_link_set
        except Exception as e:
            print(f'Problem in scraping below url:\n{search_url}\nError:\n{e.__str__()}\n')
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
            print('Jobvision job list file just created\n')
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
            print('Successfully entered job urls into file\n')
            return True
        except Exception as e:
            print('A problem happend:\n', e.__str__(), '\n')
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
            print('Successfully read job urls from the file\n')
        except Exception as e:
            print('A problem happend:\n', e.__str__(), '\n')
        return job_link_set



class ExtractRawJob:
    """In job page, extract all raw data from a single_page page."""
    def __init__(self, driver: WebDriver, job_url: str) -> None:
        """'driver' contains the html data from job_url"""
        self.driver = driver
        self.job_url = job_url
    
    
    def start_extraction(self, title:bool=True, company_name:bool=True, company_link:bool=True,
                        salary:bool=True, experience:bool=True, age:bool=True, education:bool=True,
                        skills:bool=True, gender:bool=True, language:bool=True, description:bool=True) -> dict:
        """Start extracting data from a job page in jobvision. Return result as a dict"""
        try:
            _result_dict = {'title': None, 'url': self.job_url, 'company_name': None, 'company_link': None,
                            'salary': None, 'experience': None, 'age': None, 'education': None,
                            'skills': None, 'gender': None, 'language': None, 'description': None}
            
            if title:
                _result_dict.update({'title': self.find_job_title()})
            company_name, company_link = self.find_company_name_link()
            if company_name:
                _result_dict.update({'company_name': company_name})
            if company_link:
                _result_dict.update({'company_link': company_link})
            if salary:
                _result_dict.update({'salary': self.find_offered_salary()})
            if experience:
                _result_dict.update({'experience': self.find_experience_needed()})
            if age:
                _result_dict.update({'age': self.find_age_suggestion()})
            if education:
                _result_dict.update({'education': self.find_education()})
            if skills:
                _result_dict.update({'skills': self.find_skills_needed()})
            if gender:
                _result_dict.update({'gender': self.find_gender()})
            if language:
                _result_dict.update({'language': self.find_language()})
            if description:
                _result_dict.update({'description': self.find_job_describe()})
        except KeyboardInterrupt as e:
            print('Error in "joblistings.jobvision_ir.ExtractJob.start_extraction":', '\n', e.__str__(), '\n')
        return _result_dict
    
    
    def find_job_title(self, title_selector:str='h1') -> str:
        """Find job title. Return job title as str"""
        # job_title_css_selector="h1"
        title = str()
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, title_selector).text
        except Exception as e:
            print(f'Alert: Could not find the "job title":\n{e.__str__()}\n')
            # print(f'Alert: Could not find the "job title"\n')
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
            print(f'Alert: Could not find the "company name" and "company link:\n{e.__str__()}\n')
            # print(f'Alert: Could not find the "company name" and "company link"\n')
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
            # print(f'Alert: Could not find "salary offered":\n{e.__str__()}\n')
            print(f'Alert: Could not find "salary offered":\n')
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
                # print(f'Alert: Could not find "experience":\n{e.__str__()}\n')
                print(f'Alert: Could not find "experience":\n')
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
            # print(f'Alert: Could not find "age suggestion":\n{e.__str__()}\n')
            print(f'Alert: Could not find "age suggestion":\n')
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
            # print(f'Alert: Could not find "gender": {e.__str__()}\n')
            print(f'Alert: Could not find "gender"\n')
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
            # print(f'Alert: Could not found "language": {e.__str__()}\n')
            print(f'Alert: Could not found "language"\n')
        return lang
    
    
    def find_skills_needed(self, skills_selector:str='.row.col-11.px-0 div') -> list[str]:
        """Find needed skills"""
        skills_list = list()
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, skills_selector)
            for e in elements:
                skills_list.append(e.text.replace('-', ':'))
        except Exception as e:
            # print(f'Alert: Could not find the "skills": {e.__str__()}\n')
            print(f'Alert: Could not find the "skills"\n')
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
            # print(f'Alert: Could not find the "education": {e.__str__()}\n')
            print(f'Alert: Could not find the "education"\n')
        return education
    
    
    def find_job_describe(self, job_describe_selector:str='.col-12.row.text-black.px-0.mb-3') -> str:
        """Find job description. Return it as string. If not found return empty string"""
        job_describe = str()
        try:
            job_describe = self.driver.find_element(By.CSS_SELECTOR, job_describe_selector).text.strip()
        except Exception as e:
            # print(f'Alert: Could not find "job description": {job_describe}\n')
            print(f'Alert: Could not find "job description"\n')
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
                print('No education found for the job...\n')
            # Process each job separately. 'education_list' is like this:
            # ['Bachelor : Computer and IT' , 'Bachelor : Electrical Engineering' , 'Bachelor : Finance/Accounting']
            for _education_str in _education_list:
                degree, course = _education_str.split(':')
                degree = degree.strip()
                course = course.strip()
                # ! Check if there are more than one education is in the 'course' separated by '/' (For now we ignore separation)
                # !!!!!!!!!!!!!    MORE PROCESS HERE IF NEEDED    !!!!!!!!!!!!!!!!!
                
                degree = equivalence_education_degree(degree)
                course = equivalence_education_course(course)
                
                education_list_processed.append([degree, course])
        except Exception as e:
            print('Error in joblistings.jobvision.ProcessExtractedJobData.education:\n', e.__str__(), '\n')
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
                
                skill_name = equivalence_skill_name(skill_name)
                skill_level = equivalence_skill_level(skill_level)
                
                skill_list_processed.append([skill_name, skill_level])
        except Exception as e:
            print('Error in joblistings.jobvision.ProcessExtractedJobData.skill:\n', e.__str__(), '\n')
        return skill_list_processed
    
    
    def description(self) -> object:
        pass



# ???????????????????????????????????   Independent functions   ???????????????????????????????????

def normalize_data_for_db(raw_data: dict) -> dict:
    """Before insert extracted data from the job link into db, we should normalize it."""
    try:
        normalized_data = dict()
        normalized_data.update({
            'title': raw_data['title'],
            'url': raw_data['url'],
            'company_name': raw_data['company_name'],
            'company_link': raw_data['company_link'],
            'salary_min': raw_data['salary'][0],
            'salary_max': raw_data['salary'][1],
            'experience': raw_data['experience'],
            'age_min': raw_data['age'][0],
            'age_max': raw_data['age'][1],
            'gender': raw_data['gender'],
            'language': raw_data['language'],
            'description': raw_data['description'],
            'education': raw_data['education'],
            'skill': raw_data['skills'],
        })
        
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.ExtractJob._normalize_data_for_db":\n', e.__str__(), '\n')
        
    return normalized_data



def insert_data_into_sqlite(sqlite_connector: SqliteConnection, normalized_data: dict) -> bool:
    """Insert normalized data into sqlite database."""
    try:
        # Insert data into tables
        proccess_data_dict = {'education': normalized_data.pop('education'), 'skill': normalized_data.pop('skill')}
        job_id = sqlite_connector.insert_job(data=normalized_data)
        print('job_id: ', job_id)
        pej: ProcessExtractedJobData = ProcessExtractedJobData(data=proccess_data_dict)
        
        # Insert 'education' into db
        education_list = pej.education()
        for edu_list in education_list:
            edu_data = {'degree': edu_list[0], 'course': edu_list[1]}
            education_id = sqlite_connector.insert_education(data=edu_data, job_id=job_id)
            # print('education_id: ', education_id)
            
        # Insert 'skill' into db
        skill_list = pej.skill()
        for ski_list in skill_list:
            ski_data = {'skill_name': ski_list[0], 'skill_level': ski_list[1]}
            skill_id = sqlite_connector.insert_skill(data=ski_data, job_id=job_id)
            # print('skill_id: ', skill_id)
            
        return True
    except Exception as e:
        print(f'Error in "joblistings.jobvision_ir.ExtractJob.insert_data_into_sqlite":\n{e.__str__()}\n')
        return False



# ???????????????????????????????????   Equivalence functions ?????????????????????????????????????

def equivalence_education_degree(degree: str) -> str:
    """Equivalence education degree to a standard value."""
    try:
        if degree in _equivalence.EDUCATION_DEGREE.keys():
            degree = _equivalence.EDUCATION_DEGREE[degree]
    
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.equivalence_education_degree"')
    
    return degree



def equivalence_education_course(course: str) -> str:
    """Equivalence education course to a standard value."""
    try:
        if course in _equivalence.EDUCATION_COURSE.keys():
            course = _equivalence.EDUCATION_COURSE[course]
    
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.equivalence_education_course"')
    
    return course



def equivalence_skill_name(skill_name: str) -> str:
    """Equivalence skill name to a standard value."""
    try:
        if skill_name in _equivalence.SKILL_NAME.keys():
            skill_name = _equivalence.SKILL_NAME[skill_name]
    
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.equivalence_skill_name"')
    
    return skill_name



def equivalence_skill_level(skill_level: str) -> str:
    """Equivalence skill level to a standard value."""
    try:
        if skill_level in _equivalence.SKILL_LEVEL.keys():
            skill_level = _equivalence.SKILL_LEVEL[skill_level]
    
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.equivalence_skill_level"')
    
    return skill_level
