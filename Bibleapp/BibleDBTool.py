from operator import and_
import sqlalchemy


class SqliteBible():
    def __init__(self):
        self.db = 'sqlite:///bible-sqlite.db'
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()
        self.metadata = sqlalchemy.MetaData()
        self.bible = sqlalchemy.Table(
            't_kjv',
            self.metadata,
            autoload=True,
            autoload_with=self.engine
            )
        self.books = {
            "GEN": "1",
            "EXO": "2",
            "LEV": "3",
            "NUM": "4",
            "DUE": "5",
            "JOSH": "6",
            "JUDG": "7",
            "RUTH": "8",
            "1SAM": "9",
            "2SAM": "10",
            "1KNG": "11",
            "2KNG": "12",
            "1CHR": "13",
            "2CHR": "14",
            "EZRA": "15",
            "NEH": "16",
            "ESTH": "17",
            "JOB": "18",
            "PSALM": "19",
            "PRVB": "20",
            "ECCL": "21",
            "SONG": "22",
            "ISA": "23",
            "JER": "24",
            "LAM": "25",
            "EZE": "26",
            "DAN": "27",
            "HOS": "28",
            "JOEL": "29",
            "AMOS": "30",
            "OBA": "31",
            "JONAH": "32",
            "MICAH": "33",
            "NHM": "34",
            "HBK": "35",
            "ZEPH": "36",
            "HAG": "37",
            "ZECH": "38",
            "MAL": "39",
            "MATT": "40",
            "MARK": "41",
            "LUKE": "42",
            "JHN": "43",
            "ACTS": "44",
            "ROM": "45",
            "1CRN": "46",
            "2CRN": "47",
            "GAL": "48",
            "EPH": "49",
            "PHLP": "50",
            "COL": "51",
            "1THS": "52",
            "2THS": "53",
            "1TIM": "54",
            "2TIM": "55",
            "TIT": "56",
            "PHLM": "57",
            "HEB": "58",
            "JMS": "59",
            "1PTR": "60",
            "2PTR": "61",
            "1JHN": "62",
            "2JHN": "63",
            "3JHN": "64",
            "JUDE": "65",
            "REV": "66"
        }

    def getDBResultSet(self):
        resultSet = []
        query = sqlalchemy.select([self.bible])
        resultProxy = self.connection.execute(query)
        resultSet = resultProxy.fetchall()
        return resultSet

    def formatBookNum(self, rawBook):
        if len(self.books[rawBook]) == 1:
            bookNum = '0' + self.books[rawBook]
        else:
            bookNum = self.books[rawBook]
        return bookNum

    def formatVerse(self, rawVerse):
        if len(str(rawVerse)) == 1:
            verseNum = '00{verse}'.format(verse=str(rawVerse))
        elif len(str(rawVerse)) == 2:
            verseNum = '0{verse}'.format(verse=str(rawVerse))
        else:
            verseNum = str(rawVerse)
        return verseNum

    def formatChapter(self, rawChapter):
        if len(str(rawChapter)) == 1:
            chapterNum = '00{chapter}'.format(chapter=str(rawChapter))
        elif len(str(rawChapter)) == 2:
            chapterNum = '0{chapter}'.format(chapter=str(rawChapter))
        else:
            chapterNum = rawChapter
        return chapterNum

    def getBibleVerse(self, book, chapter, verse):
        chapterNum = self.formatChapter(chapter)
        verseNum = self.formatVerse(verse)
        bookNum = self.formatBookNum(book)
        query = sqlalchemy.select([self.bible]).where(
            self.bible.columns.id == '{book}{chapter}{verse}'.format(
                book=bookNum,
                chapter=chapterNum,
                verse=verseNum)
            )
        queryProxy = self.connection.execute(query)
        queryResult = queryProxy.one()
        return '[' + str(verse) + ']' + queryResult[4]

    def getBibleChapter(self, book, chapter):
        query = sqlalchemy.select([self.bible]).filter(
            and_(
                self.bible.columns.b == self.books[book],
                self.bible.columns.c == chapter
                )
            )
        queryProxy = self.connection.execute(query)
        queryResult = queryProxy.fetchall()
        text = ''
        count = 1
        for result in queryResult:
            text += '[' + str(count) + ']' + result[4]
            count += 1
        return text

    def getBibleBook(self, book):
        bibleText = ''
        currentChapter = 0
        firstRun = True
        query = sqlalchemy.select([self.bible]).filter(
            self.bible.columns.b == self.books[book]
        )
        queryProxy = self.connection.execute(query)
        queryResult = queryProxy.fetchall()
        for row in queryResult:
            ref, bookNum, chapter, verse, text = row
            if firstRun:
                bibleText += '[{book}][Chapter 1][1]'.format(book=book) + text
                firstRun = False
                currentChapter += 1
                continue
            if chapter != currentChapter:
                bibleText += '\n[Chapter {chapter}][{verse}]{text}'.format(
                    chapter=str(chapter),
                    verse=str(verse),
                    text=text
                )
                currentChapter += 1
            else:
                bibleText += '\n[{verse}]{text}'.format(verse=verse, text=text)
        return bibleText
