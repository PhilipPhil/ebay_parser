from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Book import Book

app = Flask(__name__)
app.config['Books'] = 'sqlite://Books.db'

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)