import unittest
import sqlite3


class TestDataBase(unittest.TestCase):

    CONN = sqlite3.connect(r'data/cards.db')  # Connect to DataBase
    CURSOR = CONN.cursor()  # Create cursor

    def test_records(self):
        self.CURSOR.execute('SELECT * FROM cards')
        self.assertGreater(len(self.CURSOR.fetchmany(3)), 0)


if __name__ == '__main__':
    unittest.main()
