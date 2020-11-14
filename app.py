from flask import Flask, render_template, url_for, request, redirect, flash
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import threading
import run
import Search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.db'
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		try:
			files = request.files.getlist('files')
			db.session.query(Search.Search).delete()
			for f in files:
				searches = pd.read_excel(f)
				searches = pd.DataFrame(searches, columns=['book_id', 'max_price'])
				for search, row in searches.T.iteritems():
					new_search = Search.Search(book_id=row['book_id'], max_price=row['max_price'])
					db.session.add(new_search)
			db.session.commit()
			# print(Search.Search.query.all())
			return '<h1 style="text-align:center">Upload successful</h1>'
		except:
			return '<h1 style="text-align:center">There was an issue adding your files.</h1>'

	else:
		return render_template('index.html')


if __name__ == "__main__":
	thread1 = threading.Thread(target=run.execute_scraper)
	thread1.start()
	app.run(debug=True)
