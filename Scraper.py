from Book import Book
from Token import Token
import requests
import json
from app import Search
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from BannedSellers import BannedSellers

class Scraper:

    from_mail = 'ebayalert123@gmail.com'
    password_mail = 'sfoxktdmsbauccqa'
    # to_mail = 'sethbaker51@gmail.com'
    to_mail = 'philipgarabandic@gmail.com'

    def __init__(self):
        self.urls_sent = set()
        self.Token = Token()
        self.banned_sellers = '|'.join(BannedSellers)

    def check_books(self, book_id, max_price):
        request_url = 'https://api.ebay.com/buy/browse/v1/item_summary/search?q={book_id}&filter=price:[..{max_price}],priceCurrency:USD,excludeSellers:{{ {banned_sellers} }} '.format(book_id=book_id, max_price=max_price, banned_sellers=self.banned_sellers)

        headers = {
            'Authorization': 'Bearer ' + self.Token.get_token()
        }

        response = requests.get(url=request_url, headers=headers)
        response_json = response.json()
        books = []
        if response_json['total'] > 0:
            items = response_json['itemSummaries']
            for item in items:
                price = float(item['price']['value'])
                # shipping_service_cost = float(item['shippingOptions']['shippingCost']['value']) if item['shippingOptions']['shippingCost'] is not None else 'Unknown'
                shipping_service_cost = 'N/A'
                title = item['title']
                book_url = item['itemWebUrl']
                book_json = item
                book = Book(book_id, max_price, price, shipping_service_cost, title, book_url, book_json)
                books.append(book)
        return books

    def run(self):
        while True:
            rows = Search.Search.query.all()
            for row in rows:
                books = self.check_books(row.book_id, row.max_price)
                for book in books:
                    self.send_email(book)

    def send_email(self, book):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.from_mail, self.password_mail)

        msg = MIMEMultipart('mixed')
        msg['Subject'] = 'Book Alert'
        msg['From'] = self.from_mail
        msg['To'] = self.to_mail

        if book.url not in self.urls_sent:
            self.urls_sent.add(book.url)           
            html_mail = self.email_html(book)
            text_json = json.dumps(book.book_json, indent=4)
            msg.attach(MIMEText(html_mail, 'html'))
            msg.attach(MIMEText(text_json, 'plain'))
            server.sendmail(self.from_mail, self.to_mail, msg.as_string())
            print('Book URL: ' + book.url)

        server.quit()

    def email_html(self, book):
        html_mail = """\
        <html>
        <head>
            <style>
                table,
                th,
                td {
                    padding: 10px;
                    border: 1px solid black;
                    border-collapse: collapse;
                }
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <th>Book ID</th>
                    <th>Title</th>
                    <th>Max Price</th>
                    <th>Price</th>
                    <th>Shipping Cost</th>
                    <th>URL</th>
                </tr>
                <tr>
                    <th>"""+book.book_id+"""</th>\
                    <th>"""+book.title+ """</th>\
                    <th>"""+str(book.max_price)+"""</th>\
                    <th>"""+str(book.price)+"""</th>\
                    <th>"""+str(book.shipping_service_cost)+"""</th>\
                    <th>"""+book.url+"""</th>\
                </tr>
            </table>
        </body>
        </html>
        """
        return html_mail

    def reset_urls_sent(self):
        self.urls_sent = set()

