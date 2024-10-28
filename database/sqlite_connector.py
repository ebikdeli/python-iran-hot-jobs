import sqlite3
from sqlite3 import Connection, Cursor, OperationalError


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
                self._connect = sqlite3.connect(self.db)
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
    
    def get_or_create_extracted_data(self) -> bool:
        """Get or create "extracted_data" table"""
        try:
            _sql = f"""CREATE TABLE IF NOT EXISTS extracted_data(
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
            skills MEDIUMTEXT,
            education MEDIUMTEXT,
            description MEDIUMTEXT,
            date DATE
            );"""
            self._cursor.execute(_sql)
            return True
        except Exception as e:
            print('Error happened in access to "extracted_data" table:\n', e.__str__())
            return False
    
    def insert_into_extracted_data(self) -> bool:
        """Insert "extracted_data" table"""
        
