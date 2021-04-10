import undetected_chromedriver.v2 as uc
import pandas as pd
import time

ACCOUNT = {'email' : 'youremail@gmail.com',
            'password' : 'yourpassword'}

class Undetected_WishList:
    sleep_time = 1

    def __init__(self):
        self.driver = uc.Chrome()

    def run(self):
        self.login()
        book_ids = pd.read_csv('book_list.csv')['book_id']
        time.sleep(self.sleep_time)
        for book_id in book_ids:
            self.book_logic(book_id)
        
        time.sleep(self.sleep_time)
        print('Finished: Exit')

    def login(self):
        try:
            login_url = 'https://www.betterworldbooks.com/account/login'
            with self.driver:
                self.driver.get(login_url)
            time.sleep(self.sleep_time)
            email = self.driver.find_element_by_id('loginEmail')
            email.send_keys(ACCOUNT['email'])
            password = self.driver.find_element_by_id('loginPassword')
            password.send_keys(ACCOUNT['password'])
            sign_in = self.driver.find_elements_by_class_name('btn-success')[2]
            sign_in.click()
        except:
            time.sleep(self.sleep_time)
            self.run()

    def book_logic(self, book_id):
        try:
            self.search_logic(book_id)
            self.go_to_book()
            self.add_book_wishlist()
            print('Added to wishlist: ' + book_id)
        except:
            print('Not Found: ' + book_id)
        
    def search_logic(self, book_id):
        book_url = "https://www.betterworldbooks.com/search/results?q=" + book_id
        self.driver.get(book_url)
        time.sleep(self.sleep_time)
    
    def go_to_book(self):
        see_details = self.driver.find_element_by_class_name('thumbnail')
        see_details.click()
        time.sleep(self.sleep_time)

    def add_book_wishlist(self):
        add_to_wishlist = self.driver.find_elements_by_class_name('btn-link')[1]
        add_to_wishlist.click()
        time.sleep(self.sleep_time)

if __name__ == "__main__":
    Undetected_WishList = Undetected_WishList()
    Undetected_WishList.run()
