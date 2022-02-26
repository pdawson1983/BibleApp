import sqlite3
from BibleAPITools import getBible

conn = sqlite3.connect('BibleData')
c = conn.cursor()

c.execute(
    '''
    CREATE TABLE IF NOT EXISTS kjv_bible
    (
    [book] TEXT,
    [chapter] INTEGER,
    [verse] INTEGER,
    [text] TEXT
    )'''
    )

bible = getBible()

chapterAndVerseDict = bible.getBookAndVerseDict()
valuesForTable = []
for book in chapterAndVerseDict:
    for chapter in chapterAndVerseDict[book]:
        for verse in chapter:
            chapterInfo = verse[0].split('.')
            chapterID = chapterInfo[1]
            count = 1
            for _ in range(verse[1]):
                verseRef = verse[0] + '.' + str(count)
                valuesForTable.append((
                    book,
                    chapterID,
                    count,
                    bible.getBibleText(verseRef).strip())
                )
                count += 1

c.executemany('insert into kjv_bible values (?,?,?,?)', valuesForTable)
conn.commit()
