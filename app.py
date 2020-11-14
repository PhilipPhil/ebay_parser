from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Scraper import Scraper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
db = SQLAlchemy(app)

class Search(db.Model):
    book_id = db.Column(db.String(), primary_key=True)
    content = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = [['1234',30],['123',40]]
        
        scraper = Scraper()
        scraper.add_books('1449690777', 100)
        scraper.send_email()

    else:

        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)