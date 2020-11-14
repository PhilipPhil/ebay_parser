class Email:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def email_get_books(self):
        return self.books

    def send(self):
        print("Sending Email")
        for book in self.books:
            print('________')
            print('book_id: ' + book.book_id)
            print('title: ' + book.title)
            print('max_price: ' + str(book.max_price))
            print('price: ' + str(book.price))
            print('url: ' + book.url)

        