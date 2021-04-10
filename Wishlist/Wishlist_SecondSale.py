from selenium import webdriver
import pandas as pd
import time
from playsound import playsound

ACCOUNT = {'email' : 'youremail@gmail.com',
            'password' : 'yourpassword'}

class WishList:

    sleep_time = 2

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1280,800")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        self.browser = webdriver.Chrome(executable_path='./chromedriver',options=options)

    def run(self):
        book_ids = pd.read_csv('book_list.csv')['book_id']
        self.login()
        for book_id in book_ids:
            self.logic_book(book_id)
    
    def login(self):
        try:
            login_url = 'https://www.secondsale.com/login'
            self.browser.get(login_url)
            email = self.browser.find_element_by_name('email')
            email.send_keys(ACCOUNT['email'])
            password = self.browser.find_element_by_name('password')
            password.send_keys(ACCOUNT['password'])
            sign_in = self.browser.find_element_by_xpath("//button[@data-link-action='sign-in']")
            sign_in.click()
        except:
            time.sleep(self.sleep_time)
            self.run()

    def logic_book(self, book_id):
        try:
            self.search_logic(book_id)
        except:
            print('Not Found: ' + book_id)
    
    def search_logic(self, book_id):
        if self.search_url(book_id):
            self.go_to_book()
            self.add_book(book_id)
            
    def search_book(self, book_id):
        if self.search_url(book_id):
            return True
        else:
            return False
    
    def search_url(self, book_id):
        try:
            book_url = 'https://www.secondsale.com/search?controller=search&s=' + book_id
            self.browser.get(book_url)
            return True
        except:
            return False
        
    def go_to_book(self):
        book = self.browser.find_element_by_class_name('thumbnail-container')
        book_link = book.find_element_by_tag_name('a').get_attribute('href')
        self.browser.get(book_link)

    def add_book(self, book_id):
        buttons = self.browser.find_elements_by_id('wishlist_button')
        print(len(buttons))
        if len(buttons) == 3:
            wish_book = buttons[1]
        elif len(buttons) == 1:
            wish_book = buttons[0]
        wish_book.click()
        print('Found: ' + book_id)


if __name__ == "__main__":
    wish_list = WishList()
    wish_list.run()
