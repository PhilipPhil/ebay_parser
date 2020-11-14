from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from Book import Book

class Scraper:

    ID_APP = 'TheKaize-ASINAler-PRD-12eb4905c-db637f64'

    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def add_books(self, book_id, max_price):
        api = finding(appid=self.ID_APP, config_file=None)
        api_request = { 'keywords': book_id }
        response = api.execute('findItemsByKeywords', api_request)
        soup = BeautifulSoup(response.content,'lxml')
        items = soup.find_all('item')

        for item in items:
            price = int(round(float(item.currentprice.string)))
            title = item.title.string.lower()
            url = item.viewitemurl.string.lower()

            if price < max_price:
                book = Book(book_id, max_price, price, title, url)
                self.add_book(book)

    def email_get_books(self):
        return self.books

    def send_email(self):
        print("Sending Email")
        for book in self.books:
            print('________')
            print('book_id: ' + book.book_id)
            print('title: ' + book.title)
            print('max_price: ' + str(book.max_price))
            print('price: ' + str(book.price))
            print('url: ' + book.url)