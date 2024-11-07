from importlib import import_module
import tldextract
import os
import time
import validators



def main(check_domain: bool=True) -> None:
    # ! 1- Enter website url and process it
    website_codes = {'1': 'jobvision.ir'}
    specific_link = str()
    
    try:
        while True:
            enter_number = input('\nWebsite codes to scrap:\nPress "1" for "jobvision.ir".\nTo quit press "n": ')
            if enter_number.strip().lower() == 'n':
                print('\nProgram terminated...')
                exit()
            elif enter_number.strip() not in website_codes.keys():
                print("\nPlease enter a correct number")
                continue
            
            # ! 2- Check if user want just a job link to scrap or the whole website to be scrapped
            while True:
                just_one_link = input(f"""\nPress "any" key to scrap all the jobs in "{website_codes[enter_number]}"\n
Press "2" to scrap just one job link in "{website_codes[enter_number]}"\n
To quit press "n": """)
                if just_one_link.strip().lower() == 'n':
                    print('\nProgram terminated...')
                    exit()
                elif just_one_link.strip() == '2':
                    specific_link = input('\nEnter the job link you want to scrap: ')
                    # Validate the 'specific_link'
                    if (not validators.url(specific_link) or website_codes[enter_number] not in specific_link) and check_domain:
                        print(f'\nEnter a valid url for "{website_codes[enter_number]}"...')
                        continue
                    else:
                        print(f'\nThe job url\n"{specific_link}"\nwill be scrapped...')
                        break
                else:
                    print(f'\n"{website_codes[enter_number]}" will be scrapped...')
                    break
                
            # Following 'break' command belongs to the first 'While' loop
            break
        
        site_url = 'https://' + website_codes[enter_number]
        # Check if the received url is in the 'joblistings' directory
        domain_name = tldextract.extract(site_url)
        joblisting_module = domain_name.domain + '_' + domain_name.suffix
        joblisting_directory = f'{os.getcwd()}/joblistings'
        if not f'{joblisting_module}.py' in os.listdir(joblisting_directory):
            print(f'"{joblisting_module}" is not in the joblisting directory')
            return -1
    
        # ! 3- Call the joblising website module
        module = import_module(f'joblistings.{joblisting_module}')
        ew = module.ExtractWebsite(site_url=site_url, single_link=specific_link)
        result: str = ew.start()
        print(result)
        
    except Exception as e:
        print(f'Error: Cannot extract data from "{joblisting_module}"\n{e.__str__()}')



if __name__ == '__main__':
    main(check_domain=False)
