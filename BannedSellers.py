import app
db = app.db

class BannedSellers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    banned_seller = db.Column(db.String(), nullable=False)