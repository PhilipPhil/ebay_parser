import pandas as pd

data = pd.read_excel('./sample.xlsx')
df = pd.DataFrame(data, columns= ['book_id','max_price'])

for search, row in df.T.iteritems():
    print(row['book_id'],row['max_price'])
