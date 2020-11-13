from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from Book import Book

ID_APP = 'TheKaize-ASINAler-PRD-12eb4905c-db637f64'

def search(book):

    api = finding(appid=ID_APP, config_file=None)
    api_request = { 'keywords': book.book_id }
    response = api.execute('findItemsByKeywords', api_request)
    soup = BeautifulSoup(response.content,'lxml')
    items = soup.find_all('item')

    for item in items:
        cat = item.categoryname.string.lower()
        title = item.title.string.lower()
        price = int(round(float(item.currentprice.string)))
        url = item.viewitemurl.string.lower()

        if price < book.max_price:
            print('________')
            print('cat: ' + cat)
            print('title: ' + title)
            print('price: ' + str(price))
            print('url: ' + url)


if __name__ == "__main__":
    print('search function')
    