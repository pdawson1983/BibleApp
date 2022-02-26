import BibleDBTool


class Bible():
    """
    Bible class gathers bible text and stores
    it in the text variable
    """
    def __init__(self):
        self.text = ''
        self.bibleDB = BibleDBTool.SqliteBible()

    def getVerse(self, book, chapter, verse):
        self.text += self.bibleDB.getBibleVerse(book, chapter, verse)

    def getChapter(self, book, chapter):
        self.text += "[Chapter {ch}]".format(
            ch=chapter
            ) + self.bibleDB.getBibleChapter(book, chapter)

    def getBook(self, book):
        self.text += self.bibleDB.getBibleBook(book)

    def read(self):
        return self.text
