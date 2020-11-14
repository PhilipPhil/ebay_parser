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
            print('title: ' + book.title)
            print('price: ' + str(book.price))
            print('url: ' + book.url)

        