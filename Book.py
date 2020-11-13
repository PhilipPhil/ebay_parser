from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup

ID_APP = 'TheKaize-ASINAler-PRD-12eb4905c-db637f64'

class Book:
    def __init__(self, book_id, max_price):
        self.book_id = book_id
        self.max_price = max_price

    def search(self):

        api = finding(appid=ID_APP, config_file=None)
        api_request = { 'keywords': self.book_id }
        response = api.execute('findItemsByKeywords', api_request)
        soup = BeautifulSoup(response.content,'lxml')
        items = soup.find_all('item')

        for item in items:
            title = item.title.string.lower()
            price = int(round(float(item.currentprice.string)))
            url = item.viewitemurl.string.lower()

            if price < self.max_price:
                print('________')
                print('title: ' + title)
                print('price: ' + str(price))
                print('url: ' + url)