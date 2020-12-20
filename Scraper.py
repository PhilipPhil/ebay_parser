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

    def check_books(self, book_id, max_price):
        request_url = """https://api.ebay.com/buy/browse/v1/item_summary/search?q={book_id}&filter=price:[..{max_price}],\
        priceCurrency:GBP,itemLocationCountry:GB,excludeSellers:{{ {banned_sellers} }}""".format(book_id=book_id, max_price=max_price, banned_sellers=self.banned_sellers)

        headers = {
            'Authorization': 'Bearer ' + self.Token.get_token()
        }
        
        books = []

        try:
            response = requests.get(url=request_url, headers=headers)
            response_json = response.json()
            print("request_url: " + request_url)
            if response_json['total'] > 0:
                items = response_json['itemSummaries']
                for item in items:
                    try:
                        book_json = item
                        price = item['price']
                        title = item['title']
                        book_url = item['itemWebUrl']
                        try:
                            shipping_information = json.dumps(item['shippingOptions'], indent=4)
                        except:
                            shipping_information = 'NOT FOUND'
                        book = Book(book_id, max_price, price, shipping_information, title, book_url, book_json)
                        books.append(book)
                    except:
                        print('error with book: ' + str(item))
        except:
            print('Out of API calls: ' + str(time.time()))
            print('Pausing 60 seconds')
            time.sleep(60)

        return books

    def run(self):
        while True:
            rows = Search.Search.query.all()
            for row in rows:
                books = self.check_books(row.book_id, row.max_price)
                for book in books:
                    self.send_email(book)

    def send_email(self, book):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_settings['from_mail'], email_settings['password_mail'])

            msg = MIMEMultipart('mixed')
            msg['Subject'] = 'Book Alert'
            msg['From'] = email_settings['from_mail']
            msg['To'] = 'ebayalert123_subscriber'

            if book.url not in self.urls_sent:         
                html_mail = self.email_html(book)
                text_json = json.dumps(book.book_json, indent=4)
                msg.attach(MIMEText(html_mail, 'html'))
                msg.attach(MIMEText(text_json, 'plain'))
                server.sendmail(email_settings['from_mail'], email_settings['to_mail'], msg.as_string())
                self.urls_sent.add(book.url)
                print('Emailed Book: ' + book.url)

            server.quit()
        except:
            print('Email Failed to send: ' + book.url)

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