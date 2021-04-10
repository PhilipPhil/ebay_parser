from selenium import webdriver
import pandas as pd
import time
import os
from playsound import playsound

ACCOUNT = {'email' : 'youremail@gmail.com',
            'password' : 'yourpassword'}

class WishList:

    sleep_time = 60

    def __init__(self):
        self.count = 0
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument("window-size=1280,800")
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        self.browser = webdriver.Chrome(executable_path='./chromedriver',options=option)

    def run(self):
        book_ids = pd.read_csv('book_list.csv')['book_id']
        self.login()
        for book_id in book_ids:
            self.logic_book(book_id)
    
    def login(self):
        try:
            login_url = 'https://www.thriftbooks.com/account/login/'
            self.browser.get(login_url)
            email = self.browser.find_element_by_id('ExistingAccount_EmailAddress')
            email.send_keys(ACCOUNT['email'])
            password = self.browser.find_element_by_id('ExistingAccount_Password')
            password.send_keys(ACCOUNT['password'])
            sign_in = self.browser.find_element_by_class_name('LoginBox-submitButton--existingUser')
            sign_in.click()
        except:
            time.sleep(self.sleep_time)
            self.run()

    def logic_book(self, book_id):
        try:
            self.search_logic(book_id)
        except:
            self.is_captcha(book_id)
    
    def search_logic(self, book_id):
        if self.search_book(book_id):
            self.all_editions()
            self.add_book(book_id)

    def search_book(self, book_id):
        if self.search_box(book_id):
            return True
        elif self.search_url(book_id):
            return True
        else:
            return False

    def search_box(self, book_id):
        try:
            searchbox = self.browser.find_element_by_class_name('Search-input')
            searchbox.click()
            searchbox.clear()
            searchbox.send_keys(book_id)
            search = self.browser.find_element_by_class_name('Search-submit')
            search.click()
            return True
        except:
            return False
    
    def search_url(self, book_id):
        try:
            book_url = 'https://www.thriftbooks.com/browse/?b.search=' + book_id
            self.browser.get(book_url)
            return True
        except:
            return False

    def all_editions(self):
        allEditions = self.browser.find_element_by_class_name('AdditionalFormat-text')
        allEditions.click()
    
    def add_book(self, book_id):
        book_list = self.browser.find_elements_by_class_name('AllEditionsItem-work')
        for book in book_list:
            span_list = book.find_elements_by_class_name('AllEditionsItem-details-item-details')
            for span in span_list:
                if span.get_attribute("innerHTML") == book_id:
                    wish_book = book.find_element_by_class_name('WorkWishListButton')
                    wish_book.click()
                    self.count+=1
                    print('Click: ' + str(self.count))
                    print('Found: ' + book_id)
                    break


    def is_captcha(self, book_id):
        try:
            self.browser.find_element_by_class_name('g-recaptcha-response')
            print('captcha pause')
            self.sound()
            time.sleep(self.sleep_time)
            self.is_captcha(book_id)
        except:
            self.is_captcha_logic_book(book_id)

    def is_captcha_logic_book(self, book_id):
        try:
            self.search_logic(book_id)
        except:
            print('Not Found: ' + book_id)

    def sound(self):
        for _ in range(3):
            playsound('./doh.wav')

if __name__ == "__main__":
    wish_list = WishList()
    wish_list.run()
