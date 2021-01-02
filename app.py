from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import threading
from Utilities import token_settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

import Search
from Scraper import Scraper

scraper = Scraper()

@app.before_first_request
def thread_start():
    scraper_thread = threading.Thread(target=scraper.run)
    scraper_thread.start()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['password'] == token_settings['client_secret']:
            try:
                files = request.files.getlist('files')
                db.session.query(Search.Search).delete()
                for f in files:
                    searches = pd.read_csv(f)
                    searches = pd.DataFrame(searches, columns=['book_id', 'max_price'])
                    for _, row in searches.T.iteritems():
                        new_search = Search.Search(book_id=row['book_id'], max_price=row['max_price'])
                        db.session.add(new_search)
                db.session.commit()
                return '<h1 style="text-align:center">Upload successful</h1>'
            except:
                return '<h1 style="text-align:center">There was an issue adding your files</h1>'
        else:
            return '<h1 style="text-align:center">Incorrect password</h1>'

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run()
