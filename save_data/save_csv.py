import csv
import os


def into_csv(data:dict, url:str) -> bool:
    """Save extracted data into a csv file"""
    try:
        csv_file = f'{os.getcwd()}/jobs.csv'
        fields = ['title', 'url', 'company_name', 'company_link', 'salary_min', 'salary_max',
                'experience', 'age_min', 'age_max', 'gender', 'language', 'skills',
                'education', 'description']
        data_row = [data['title'], url, data['company_name'], data['company_link'], data['salary'][0], data['salary'][1],
                    data['experience'], data['age'][0], data['age'][1], data['gender'], data['language'],
                    ' , '.join(data['skills']), ' , '.join(data['education']), data['job_description']]
        # Check if csv file not exists or does not have header in it create a new csv file with 'fields' as header
        try:
            f = open(csv_file, 'rt', encoding='utf-8')
            first_line = f.readline()
            if not first_line:
                with open(csv_file, mode='wt', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
        except Exception as e:
            with open(csv_file, mode='wt', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        # Write data into the csv file
        with open(csv_file, mode='at', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_row)
        print('Successfully data written into csv file')
    except Exception as e:
        print('Error in write data into csv file:\n', e.__str__())
        return False
    return True
