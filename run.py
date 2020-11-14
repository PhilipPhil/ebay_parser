from Email import Email
from Search import Search

email = Email()
s = Search(email)
s.search('1449690777', 100)
email.send()