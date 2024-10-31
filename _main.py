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


if __name__ == '__main__':
    main()
