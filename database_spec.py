import unittest
import os
import database as database

TEST_FILENAME = 'test_file-1'
TEST_BASEPATH = 'test-segments/'
TESTPATH = TEST_BASEPATH + TEST_FILENAME

class TestDatabase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        
        for filename in os.listdir(TEST_BASEPATH):
            os.remove(TEST_BASEPATH + filename)

    # db_set
    def test_db_set_stores_pair(self):
        db = database.Database(TEST_FILENAME, TEST_BASEPATH)
        
        db.db_set('1', 'test1')
        db.db_set('2', 'test2')

        with open(TESTPATH, 'r') as s:
            line1 = s.readline().strip()
            line2 = s.readline().strip()

        self.assertEqual(line1, '1,test1')
        self.assertEqual(line2, '2,test2')

    def test_db_set_stores_index(self):
        db = database.Database(TEST_FILENAME, TEST_BASEPATH)
        
        db.db_set('1', 'test1')
        db.db_set('2', 'test2')

        self.assertEqual(db.index['1'], 0)
        self.assertEqual(db.index['2'], 8)

    def test_db_set_index_retrieves_correct_value(self):
        db = database.Database(TEST_FILENAME, TEST_BASEPATH)
        
        db.db_set('1', 'test1')
        db.db_set('2', 'test2')
        db.db_set('3', 'test3')
        db.db_set('4', 'test4')

        with open(TESTPATH, 'r') as s:
            s.seek(db.index['2'])
            self.assertEqual(s.readline(), '2,test2\n')
            s.seek(db.index['4'])
            self.assertEqual(s.readline(), '4,test4\n')

    # db_get
    def test_db_get_retrieve_val(self):
        with open(TESTPATH, 'w') as s:
            s.write('1,test1\n')
            s.write('2,test2\n')

        db = database.Database(TEST_FILENAME, TEST_BASEPATH)

        self.assertEqual(db.db_get('1'), 'test1')
        self.assertEqual(db.db_get('2'), 'test2')
        self.assertEqual(db.db_get('3'), None)
    
    def test_db_get_retrieve_most_recent_val(self):
        with open(TESTPATH, 'w') as s:
            s.write('1,test1\n')
            s.write('2,test2\n')
            s.write('1,new value\n')
        
        db = database.Database(TEST_FILENAME, TEST_BASEPATH)
        self.assertEqual(db.db_get('1'), 'new value')

    # segments
    def test_db_set_uses_segment(self):
        db = database.Database(TEST_FILENAME, TEST_BASEPATH)
        db.threshold = 10
        db.db_set('abc', 'cba')
        db.db_set('def', 'fed') # This will cross the threshold

        self.assertEqual(db.current_segment_size, 8)
        self.assertEqual(db.current_segment, 'test_file-2')

if __name__ == '__main__':
    unittest.main()