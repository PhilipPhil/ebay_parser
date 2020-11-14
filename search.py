from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from Book import Book

class Search:

    ID_APP = 'TheKaize-ASINAler-PRD-12eb4905c-db637f64'

    def __init__(self, email):
        self.email = email

    
    def search(self, book_id, max_price):
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
                self.email.add_book(book)