from database.sqlite_connector import SqlliteConnection
import sqlite3
from sqlite3 import Connection, Cursor
import unittest


class TestSqlliteConnection(unittest.TestCase):
    """Test SqlliteConnetion"""
    def setUp(self):
        self.sqlconn: SqlliteConnection = SqlliteConnection()
    
    def test_is_connect(self):
        print(self.sqlconn)
        self.assertIsNotNone(self.sqlconn)
    
    def test_is_close(self):
        self.sqlconn.close_connect()
    

# sc: SqlliteConnection = SqlliteConnection()
# # sc.get_or_create_extracted_data()
# sc.close_connect()