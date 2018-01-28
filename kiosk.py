import requests
from enum import Enum

class Status(Enum):
    AVAILABLE = 1
    CHECKED_OUT = 2
    DOES_NOT_EXIST = 3

class kiosk:
    def __init__(self):
        self.base_url = 'https://pillar.libib.com/kiosk'
        self.kiosk_url = 'https://pillar.libib.com/functions/kiosk/item-lookup.php'
        self.api_url = 'https://www.libib.com/library/functions/lending-item-lookup.php'

    def get_session_id(self, session):
        response = session.get(self.base_url)
        cookie = response.headers['Set-Cookie'].split(';')[0].split('=')[1]
        return cookie

    def find_book(self, barcode):
	with requests.session() as s:
            s.get(self.base_url)
            response = s.post(self.kiosk_url, data={'barcode': barcode}, headers={'Referer': self.base_url})
            return response.json()

    def get_book_status(self, barcode):
        book = self.find_book(barcode)
        return self.parse_status(book)

    def parse_status(self, book):
        if book.get('outcome', '') == 'fail':
            return Status.CHECKED_OUT if book.get('title') else Status.DOES_NOT_EXIST

        return Status.AVAILABLE

if __name__ == '__main__':
    test = kiosk()
    print test.get_book_status('2010000000014')
