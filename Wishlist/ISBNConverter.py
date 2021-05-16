import pyisbn
import pandas as pd


def convert_isbn10_to_13():
    book_ids = pd.read_csv('book_list.csv')['book_id']
    isbn13_list = []
    asin_list = []
    for book_id in book_ids:
        print(book_id)
        try:
            isbn10 = pyisbn.Isbn10(book_id)
        except:
            print('Not an ISBN')
            asin_list.append(book_id)

        isbn13 = isbn10.convert()
        isbn13_list.append(isbn13)
    df_isbn13 = pd.DataFrame(data={'ISBN13': isbn13_list})
    df_isbn13.to_csv('book_list13.csv', index=False)
    df_asin = pd.DataFrame(data={'ASIN': asin_list})
    df_asin.to_csv('book_list_asin.csv', index=False)


if __name__ == "__main__":
    convert_isbn10_to_13()

