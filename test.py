from io import StringIO
from unittest.mock import patch
import unittest
import main
import functions

class MainTest(unittest.TestCase):
    
    def test_db_connection(self):
        conn = functions.get_sqlite_connection('./sqlite.db')
        self.assertNotEqual(conn, -1)
    
    def test_main(self):
        with patch('sys.stdout', new=StringIO()) as main_output:
            main.main(True)
            print(main_output.getvalue().strip())
            self.assertIn('SUCCESS', main_output.getvalue().strip())
    

if __name__ == '__main__':
    unittest.main()