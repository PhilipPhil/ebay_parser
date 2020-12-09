class Book:
    def __init__(self, book_id, max_price, price, shipping_information, title, url, book_json):
        self.book_id = book_id
        self.max_price = max_price
        self.price = price
        self.shipping_information = shipping_information
        self.title = title
        self.url = url
        self.book_json = book_json