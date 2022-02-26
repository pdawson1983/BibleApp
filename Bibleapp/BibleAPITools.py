import requests


class getBible():
    def __init__(self):
        self.bibleID = 'de4e12af7f28f599-02'
        self.accessKey = '1b0d75be374e152db437131ae6c90779'

    def queryAPI(self, queryItem=''):
        apiHeaders = {
            'api-key': self.accessKey}
        response = requests.get(
            "https://api.scripture.api.bible/v1/bibles/{bibleID}/{queryItem}"
            .format(
                bibleID=self.bibleID,
                queryItem=queryItem
            ), headers=apiHeaders
            )
        return response

    def getBookAndVerseDict(self):
        bookAndVerseDict = {}
        booksJSON = self.queryAPI('books').json()
        for book in booksJSON['data']:
            chapterInfo = []
            chaptersJSON = self.queryAPI(
                'books/{bookID}/chapters'.format(bookID=book['id'])).json()
            for chapter in chaptersJSON['data']:
                versesJSON = self.queryAPI(
                    'chapters/{chapterId}/verses'
                    .format(chapterId=chapter['id'])
                ).json()
                chapterInfo.append((chapter['id'], len(versesJSON['data'])))
            bookAndVerseDict[book['id']] = [chapterInfo]
        return bookAndVerseDict

    def getBibleText(self, reference):
        verseJSON = self.queryAPI(
            'verses/{reference}?content-type=text&include'
            '-notes=false&include-titles=false&include-chapter'
            '-numbers=false&include-verse-numbers=true&include-'
            'verse-spans=false&use-org-id=false'
            .format(reference=reference)
            ).json()
        verseData = verseJSON['data']
        return verseData['content']
