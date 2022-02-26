import unittest
from BibleDBTool import SqliteBible


class TestBibleDBTool(unittest.TestCase):
    """
    This tests the BibleDBTool module and its ability to connect
    to the DB.
    """
    maxdiff = None

    def setUp(self):
        self.bibleDB = SqliteBible()

    def testGetDataFromDB(self):
        """
        Test that tool is able to access DB
        """
        results = self.bibleDB.getDBResultSet()
        self.assertTrue(results, "DB query did not give any results")


if __name__ == '__main__':
    unittest.main()
