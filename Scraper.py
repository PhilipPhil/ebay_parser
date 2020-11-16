from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from Book import Book
import time
from app import Search
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Scraper:

    ID_APP = 'TheKaize-ASINAler-PRD-12eb4905c-db637f64'

    def __init__(self):
        self.urls_sent = set()

    def check_books(self, book_id, max_price):
        api = finding(appid=self.ID_APP, config_file=None)
        time.sleep(18)
        api_request = { 'keywords': book_id }
        response = api.execute('findItemsByKeywords', api_request)
        soup = BeautifulSoup(response.content,'lxml')
        items = soup.find_all('item')

        books = []
        for item in items:
            price = int(round(float(item.currentprice.string)))
            title = item.title.string.lower()
            url = item.viewitemurl.string.lower()
            book_xml = item

            if price < max_price:
                book = Book(book_id, max_price, price, title, url, book_xml)
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
        # print("Sending Email")
        # if book.url not in self.urls_sent:
        #     self.urls_sent.add(book.url)
        #     print('________')
        #     print('book_id: ' + book.book_id)
        #     print('title: ' + book.title)
        #     print('max_price: ' + str(book.max_price))
        #     print('price: ' + str(book.price))
        #     print('url: ' + book.url)
        #     print('book_xml: ' + str(book.book_xml))
        from_mail = 'ebayalert123@gmail.com'
        password = 'sfoxktdmsbauccqa'
        to_mail = 'dealalchemist@gmail.com'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(from_mail, password)

        msg = MIMEMultipart('mixed')
        msg['Subject'] = 'Book Alert'
        msg['From'] = from_mail
        msg['To'] = to_mail

        if book.url not in self.urls_sent:
            self.urls_sent.add(book.url)
            print('________')
            print('book_id: ' + book.book_id)
            print('title: ' + book.title)
            print(book.book_xml.prettify())

            html = """\
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
                        <th>URL</th>
                    </tr>
                    <tr>
                        <th>"""+book.book_id+"""</th>\
                        <th>"""+book.title+ """</th>\
                        <th>"""+str(book.max_price)+"""</th>\
                        <th>"""+str(book.price)+"""</th>\
                        <th>"""+book.url+"""</th>\
                    </tr>
                </table>
            </body>
            </html>
            """
            text_xml = book.book_xml.prettify()

            msg.attach(MIMEText(html, 'html'))
            msg.attach(MIMEText(text_xml, 'plain')) 

            server.sendmail(from_mail, to_mail, msg.as_string())
            print('email has been sent successfully')
        server.quit()

    def reset_urls_sent(self):
        self.urls_sent = set()

