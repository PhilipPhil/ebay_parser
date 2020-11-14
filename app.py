from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
        new_search = Search(book_id = '1449690777', content = 100)
        try:
            db.session.add(new_search)
            db.session.commit()
            return 'File has been uploaded'
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)