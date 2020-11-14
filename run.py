from Scraper import Scraper
# run every 2 hours
    scraper = Scraper()
    # for data in db
        scraper.add_books('1449690777', 100)
    scraper.send_email()