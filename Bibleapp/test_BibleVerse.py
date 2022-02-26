import unittest
from BibleVerse import Bible


class TestBibleVerse(unittest.TestCase):
    """
    This tests the BibleVerse module
    """
    maxDiff = None
    gen1_1 = '[1]In the beginning God created the heaven and the earth.'
    psalm_117 = '[Chapter 117][1]O praise the LORD, all ye nations: '\
                'praise him, all ye people.[2]For his merciful kindness '\
                'is great toward us: and the truth of the LORD endureth for '\
                'ever. Praise ye the LORD.'
    with open('2PTR.txt', 'r') as file:
        secondPeter = file.read()

    def setUp(self):
        self.bible = Bible()

    def testNoVerse(self):
        """
        Test no verse being selected
        """
        self.assertEqual(
            '',
            self.bible.read(),
            "Text returned when no text should be present")

    def testSingleVerse(self):
        """
        Test getting a single verse.
        """
        self.bible.getVerse('GEN', 1, 1)
        self.assertEqual(
            self.gen1_1,
            self.bible.read(),
            "Incorrect bible verse returned")

    def testSingleChapter(self):
        """
        Test getting a single chapter.
        """
        self.bible.getChapter('PSALM', 117)
        self.assertEqual(
            self.psalm_117,
            self.bible.read(),
            "Incorrect bible chapter returned or text does not match"
        )

    def testWholeBook(self):
        """
        Test getting a whole book.
        """
        self.bible.getBook('2PTR')
        self.assertEqual(
            self.secondPeter,
            self.bible.read(),
            "Incorrect book returned or text does not match"
        )


if __name__ == "__main__":
    unittest.main()
