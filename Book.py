class Book:
    def __init__(self, book_id, max_price, price, shipping_service_cost, title, url, book_xml):
        self.book_id = book_id
        self.max_price = max_price
        self.price = price
        self.shipping_service_cost = shipping_service_cost
        self.title = title
        self.url = url
        self.book_xml = book_xml