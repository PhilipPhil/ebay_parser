from selenium import webdriver
import pandas as pd
import time

ACCOUNT = {'email' : 'cjoanne614@gmail.com',
            'password' : 'DsdUWy-C43Gq!%M'}

class WishList:

    sleep_time = 3

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("window-size=1280,800")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.browser = webdriver.Chrome(executable_path='./chromedriver',options=options)

    def run(self):
        book_ids = pd.read_csv('book_list.csv')['book_id']
        if not self.login():
            print("Login Failed")
            return
        for book_id in book_ids:
            self.logic_book(book_id)
    
    def login(self):
        try:
            login_url = 'https://www.worldofbooks.com'
            self.browser.get(login_url)
            time.sleep(self.sleep_time)
            
            cookie_button = self.browser.find_element_by_class_name('Cookie__buttons')
            cookie_button.click()
            print('cookie')

            account = self.browser.find_elements_by_class_name('headerMenuItem')[1]
            account.click()
            print('account')

            email = self.browser.find_elements_by_class_name('form-control')[1]
            email.send_keys(ACCOUNT['email'])
            print('email')

            password = self.browser.find_elements_by_class_name('form-control')[2]
            password.send_keys(ACCOUNT['password'])
            print('password')

            sign_in = self.browser.find_elements_by_class_name('btn')[2]
            sign_in.click()
            print('sign_in')

            time.sleep(self.sleep_time)
            
            return True
        except:
            return False

    def logic_book(self, book_id):
        try:
            self.search_logic(book_id)
        except:
            print('Not Found: ' + book_id)
    
    def search_logic(self, book_id):
        if self.search_url(book_id):
            self.add_book(book_id)
    
    def search_url(self, book_id):
        try:
            book_url = 'https://www.worldofbooks.com/en-gb/category/all?search=' + book_id
            self.browser.get(book_url)
            return True
        except:
            return False

    def add_book(self, book_id):
        button = self.browser.find_element_by_class_name('wishlistButton').find_element_by_class_name('btn')
        button.click()
        print('Found: ' + book_id)

if __name__ == "__main__":
    wish_list = WishList()
    wish_list.run()