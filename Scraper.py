from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
import requests
import json

from Utilities import BannedSellers, email_settings
from Book import Book
from Token import Token

from app import Search

class Scraper:

    def __init__(self):
        self.urls_sent = set()
        self.Token = Token()
        self.banned_sellers = '|'.join(BannedSellers)
        self.books = []
        self.time_emailed = time.time()

    def check_books(self, book_id, max_price):
        request_url = """https://api.ebay.com/buy/browse/v1/item_summary/search?q={book_id}&filter=price:[..{max_price}],\
        priceCurrency:GBP,itemLocationCountry:GB,excludeSellers:{{ {banned_sellers} }}""".format(book_id=book_id, max_price=max_price, banned_sellers=self.banned_sellers)

        headers = {
            'Authorization': 'Bearer ' + self.Token.get_token()
        }
        
        try:
            response = requests.get(url=request_url, headers=headers)
            response_json = response.json()
            print("request_url: " + request_url)
            if response_json['total'] > 0:
                items = response_json['itemSummaries']
                for item in items:
                    try:
                        book_json = json.dumps(item, indent=4)
                        book_url = item['itemWebUrl']
                        title = item['title']
                        price = json.dumps(item['price'], indent=4)
                        try:
                            shipping_information = json.dumps(item['shippingOptions'], indent=4)
                        except:
                            shipping_information = 'NOT FOUND'
                        book = Book(book_id, max_price, price, shipping_information, title, book_url, book_json)
                        if book.url not in self.urls_sent:
                            self.books.append(book)
                    except:
                        print('error with book: ' + str(item))
        except:
            print('Out of API calls: ' + str(time.time()))
            print('Pausing 60 seconds')
            time.sleep(60)

    def run(self):
        while True:
            rows = Search.Search.query.all()
            for row in rows:
                self.check_books(row.book_id, row.max_price)
                if time.time() - self.time_emailed > 5*60:
                    self.send_email()

    def send_email(self):

        if len(self.books) == 0:
            return

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_settings['from_mail'], email_settings['password_mail'])
        except:
            print('Email connection failed')
            return

        msg = MIMEMultipart('mixed')
        msg['Subject'] = 'Books found: ' + str(len(self.books))
        msg['From'] = email_settings['from_mail']
        msg['To'] = 'ebayalert123_subscriber'

        for book in self.books:
            if book.url not in self.urls_sent:         
                html_mail = self.email_html(book)
                msg.attach(MIMEText(html_mail, 'html'))
                msg.attach(MIMEText(book.book_json, 'plain'))

        try:
            server.sendmail(email_settings['from_mail'], email_settings['to_mail'], msg.as_string())
            
            for book in self.books:
                self.urls_sent.add(book.url)
                print('Emailed Book: ' + book.url)
            self.books = []
            self.time_emailed = time.time()

            server.quit()
        except:
            print('Email Failed to send')
            print('Pausing 600 seconds')
            time.sleep(600)

    def email_html(self, book):
        html_mail = """
        <html>
        <head>
            <style>
                table,
                th,
                td {{
                    padding: 10px;
                    border: 1px solid black;
                    border-collapse: collapse;
                }}
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <th>Book ID</th>
                    <th>Title</th>
                    <th>Max Price (GBP)</th>
                    <th>Price</th>
                    <th>Shipping Information</th>
                    <th>URL</th>
                </tr>
                <tr>
                    <th>{book_id}</th>
                    <th>{title}</th>
                    <th>{max_price}</th>
                    <th>{price}</th>
                    <th>{shipping_information}</th>
                    <th>{url}</th>
                </tr>
            </table>
        </body>
        </html>
        """.format(book_id=book.book_id, title=book.title, max_price=book.max_price, price=book.price,
                   shipping_information=book.shipping_information, url=book.url)
        return html_mail
        
    def reset_urls_sent(self):
        self.urls_sent = set()