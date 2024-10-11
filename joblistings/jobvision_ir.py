from drivers.selenium_driver import call_selenium_driver
from selenium.webdriver.common.by import By
from time import sleep


def extract_website(site_url: str, job_title: str='python') -> str:
    """Extract jobvision.ir jobs"""
    print(f'Call the joblisting website for the "{site_url}"')
    try:
        driver = call_selenium_driver(headless=1)
        # ! Get all the 'python' jobs
        job_cards = []
        page_number = 1
        while page_number:
            print('page number: ', page_number)
            search_url = f'https://jobvision.ir/jobs/keyword/{job_title}?page={page_number}'
            driver.get(search_url)
            sleep(1)
            job_cards.extend(driver.find_elements(By.TAG_NAME, 'job-card'))
            # ! Check if there are any page remained to process
            try:
                active_pagination_page = driver.find_element(By.CSS_SELECTOR, '.pagination-page.page-item.active')
                if active_pagination_page.text.strip() == 'آخرین':
                    break
                else:
                    page_number += 1
            except Exception as e:
                print(f'No element found as ".pagination-page.page-item.active" or no page remains')
                break
        # ! Process every 'job_cards' received
        print(f'Number of jobs found for "{job_title}" job title: {len(job_cards)}')
        
    except Exception as e:
        print(f'CANNOT OPEN "{site_url}"')
        print(e.__str__())
        # return -1
    driver.close()
    return 'OK'
