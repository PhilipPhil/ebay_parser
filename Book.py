class Book:
    def __init__(self, book_id, max_price, price, shipping, title, url, book_xml):
        self.book_id = book_id
        self.max_price = max_price
        self.price = price
        self.shipping = shipping
        self.title = title
        self.url = url
        self.book_xml = book_xml