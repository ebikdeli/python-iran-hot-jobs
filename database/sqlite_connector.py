"""Sqllite3 connection and process defined here."""
from ._helper_functions import _insert_fields_values
import sqlite3
from sqlite3 import Connection, Cursor, OperationalError
import os
import datetime


class SqlliteConnection:
    """Automate connection to sqllite db"""
    def __init__(self, db:str='hot_jobs.db'):
        """We use the approach of having a single sql cursor throught the application."""
        self.db = db
        self._connect: Connection = None
        self._cursor: Cursor = None
        self.make_connect()
        self.make_cursor()
    
    
    def make_connect(self) -> Connection|None:
        """Connect to db. Return Connection instance if successful else return None."""
        try:
            if not isinstance(self._connect, Connection):
                _db_path = os.path.join(os.path.dirname(__file__), self.db)
                self._connect = sqlite3.connect(_db_path)
            return self._connect
        except Exception as e:
            print(f'Connection did not make with "{self.db}":\n{e.__str__()}')
            return None
    
    
    def make_cursor(self) -> Cursor|None:
        """Make Cursor from connection. Return Cursor instance if successful else return None"""
        try:
            self.make_connect()
            if not isinstance(self._cursor, Cursor):
                self._cursor = self._connect.cursor()
            return self._cursor
        except Exception as e:
            print(f'Cursor did not created for db:\n{e.__str__()}')
            return None
    
    
    def close_connect(self) -> None:
        """Close connection and cursor"""
        try:
            self.close_cursor()
            self._connect.close()
        except Exception as e:
            pass
        self._connect = None
    
    
    def close_cursor(self) -> None:
        """Close connection cursor"""
        try:
            self._cursor.close()
        except Exception as e:
            pass
        self._cursor = None
    
    
    # 'job' table
    
    def get_or_create_job(self) -> bool:
        """Get or create "job" table"""
        try:
            _sql = f"""CREATE TABLE IF NOT EXISTS job(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            url VARCHAR(1000) NOT NULL,
            company_name VARCHAR(255) NOT NULL,
            company_link VARCHAR(1000),
            salary_min DECIMAL(12,0) DEFAULT 0,
            salary_max DECIMAL(12,0) DEFAULT 0,
            experience INT DEFAULT 0,
            age_min INT DEFAULT 0,
            age_max INT DEFAULT 0,
            gender VARCHAR(10),
            language VARCHAR(15),
            description MEDIUMTEXT,
            date DATE
            );"""
            self._cursor.execute(_sql)
            return True
        except Exception as e:
            print('Error happened in access to "job" table:\n', e.__str__())
            return False
    
    
    def insert_job(self, data: dict) -> int|None:
        """Insert data into "job" table. If successful return latest row 'id' of the job just inserted.\n
        "data" is a dict contains {column1: value1, column2: value2, ....}."""
        try:
            # Add 'date' field and set its value as today date
            data.update({'date': datetime.date.today().__str__()})
            _job_string_fields = ['title', 'url', 'company_name', 'company_link', 'gender', 'language', 'description', 'date']
            _job_fields, _job_values = _insert_fields_values(data, _job_string_fields)
            sql = f"INSERT INTO job({_job_fields}) VALUES({_job_values})"
            self._cursor.execute(sql)
            self._connect.commit()
            _latest_job_id = self._cursor.lastrowid
            return _latest_job_id
        except Exception as e:
            print(f'Cannot insert data into "job" table:\n{e.__str__()}\n')
            return None
    
    
    # 'education' table
    
    def get_or_create_education(self) -> bool:
        """Get 'education' table. If not exist create it. If error happend return False."""
        try:
            _sql = f"""CREATE TABLE IF NOT EXISTS education(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            degree VARCHAR(50) NOT NULL,
            course VARCHAR(60) NOT NULL,
            date DATE,
            FOREIGN KEY (job_id) REFERENCES job(id) 
            );"""
            self._cursor.execute(_sql)
            return True
        except Exception as e:
            print('Error in access "education" table:\n', e.__str__(), '\n')
            return False
    
    
    def insert_education(self, data: dict, job_id: int) -> int|None:
        """Insert data into "education" table. If successful return latest row 'id' of the education just inserted.\n
        "data" is a dict contains {column1: value1, column2: value2, ....}.\n
        "job_id" is the foreign_key field to "job.id" table and its primary_key field 'id'."""
        try:
            data.update({'job_id': job_id, 'date': datetime.date.today().__str__()})
            _education_string_fields = ['degree', 'course', 'date']
            _education_fields, _education_values = _insert_fields_values(data, _education_string_fields)
            sql = f"INSERT INTO education({_education_fields}) VALUES({_education_values})"
            self._cursor.execute(sql)
            self._connect.commit()
            _latest_education_id = self._cursor.lastrowid
            return _latest_education_id
        except Exception as e:
            print(f'Cannot insert data into "education" table:\n{e.__str__()}\n')
            return None
    
    
    # 'skill' table
    
    def get_or_create_skill(self) -> bool:
        """Get 'skill' table. If not exist create it. If error happend return False."""
        try:
            _sql = f"""CREATE TABLE IF NOT EXISTS skill(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            skill_name VARCHAR(50) NOT NULL,
            skill_level VARCHAR(60) NOT NULL,
            date DATE,
            FOREIGN KEY (job_id) REFERENCES job(id) 
            );"""
            self._cursor.execute(_sql)
            return True
        except Exception as e:
            print('Error in access "skill" table:\n', e.__str__(), '\n')
            return False
    
    
    def insert_skill(self, data: dict, job_id: int) -> int|None:
        """Insert data into "skill" table. If successful return latest row 'id' of the skill just inserted.\n
        "data" is a dict contains {column1: value1, column2: value2, ....}.\n
        "job_id" is the foreign_key field to "job.id" table and its primary_key field 'id'."""
        try:
            data.update({'job_id': job_id, 'date': datetime.date.today().__str__()})
            _skill_string_fields = ['skill_name', 'skill_level', 'date']
            _skill_fields, _skill_values = _insert_fields_values(data, _skill_string_fields)
            sql = f"INSERT INTO skill({_skill_fields}) VALUES({_skill_values})"
            self._cursor.execute(sql)
            self._connect.commit()
            _latest_skill_id = self._cursor.lastrowid
            return _latest_skill_id
        except Exception as e:
            print(f'Cannot insert data into "skill" table:\n{e.__str__()}\n')
            return None
