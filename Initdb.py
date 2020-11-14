from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
db = SQLAlchemy(app)

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(), nullable=False)
    max_price = db.Column(db.Integer, nullable=False)

new_search = Search(book_id = '1449690777', max_price = 100)
print(new_search)
db.session.add(new_search)
db.session.commit()

print(Search.query.all())

# db.create_all()