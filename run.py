from Scraper import Scraper
import time


def execute_scraper():
	book_id = 1305110706
	while True:
		scraper = Scraper()
		scraper.add_books(str(book_id), 100)
		scraper.email_get_books()
		scraper.send_email()
		book_id += 1
		time.sleep(2)


