from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
db = SQLAlchemy(app)

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(), nullable=False)
    content = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        searches = pd.read_excel('./sample.xlsx')
        searches = pd.DataFrame(searches, columns= ['book_id','max_price'])
        new_search = Search(book_id = '1449690777', content = 100)

        try:
            db.session.add(new_search)
            db.session.commit()
            return '<h1 style="text-align:center">Upload successful</h1>'
        except:
            return '<h1 style="text-align:center">There was an issue adding your file'</h1>'

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)