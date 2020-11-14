from Scraper import Scraper
import time


scraper = Scraper()
books = scraper.check_books('1305110706', 30)
for book in books:
	scraper.send_email(book)

books = scraper.check_books('1305110706', 100)
for book in books:
	scraper.send_email(book)


