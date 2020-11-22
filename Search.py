import app
db = app.db

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(), nullable=False)
    max_price = db.Column(db.Integer, nullable=False)