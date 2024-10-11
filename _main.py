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
    
    
main()