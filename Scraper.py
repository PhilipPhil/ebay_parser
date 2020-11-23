from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from Book import Book
import time
from app import Search
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Scraper:

    from_mail = 'ebayalert123@gmail.com'
    password_mail = 'sfoxktdmsbauccqa'
    # to_mail = 'sethbaker51@gmail.com'
    to_mail = 'gracia9828@gmail.com'
    ID_APP = ['SethBake-ASINAler-PRD-47c01d8ca-e867093d','TheKaize-ASINAler-PRD-12eb4905c-db637f64']

    def __init__(self):
        self.urls_sent = set()
        self.ID_Index = 1

    def get_ID_Index(self):
        self.ID_Index+=1
        if self.ID_Index > len(self.ID_APP):
            self.ID_Index = 1
        return self.ID_Index % len(self.ID_APP)

    def check_books(self, book_id, max_price):
        index = self.get_ID_Index()
        print(self.ID_APP[index])
        api = finding(appid=self.ID_APP[index], config_file=None)
        time.sleep(8.7)
        api_request = {'keywords': book_id,
                       'itemFilter': [
                           {'name': 'MaxPrice', 'value': max_price, 'paramName': 'Currency', 'paramValue': 'USD'},
                           {'name': 'ExcludeSeller',
                            'value': ['fortwaynegoodwill', 'lazilyround', 'benjkuzn_0', 'integritybooksales',
                                      'selectdiscountshop', 'discountshelf']}
                       ]}
        response = api.execute('findItemsAdvanced', api_request)
        soup = BeautifulSoup(response.content,'lxml')
        items = soup.find_all('item')
        # print(items)

        books = []
        for item in items:
            price = float(item.currentprice.string)
            if item.shippingservicecost is not None:
                shipping = float(item.shippingservicecost.string)
            else:
                shipping = 'Unknown'
            title = item.title.string.lower()
            url = item.viewitemurl.string.lower()
            book_xml = item

            book = Book(book_id, max_price, price, shipping, title, url, book_xml)
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
            text_xml = book.book_xml.prettify()

            msg.attach(MIMEText(html_mail, 'html'))
            msg.attach(MIMEText(text_xml, 'plain')) 

            server.sendmail(self.from_mail, self.to_mail, msg.as_string())
            
            print('url: ' + book.url)
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
                    <th>"""+str(book.shipping)+"""</th>\
                    <th>"""+book.url+"""</th>\
                </tr>
            </table>
        </body>
        </html>
        """
        return html_mail

    def reset_urls_sent(self):
        self.urls_sent = set()

