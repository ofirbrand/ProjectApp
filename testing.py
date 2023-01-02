from ProjectApp import connection, cursor
from ProjectApp.routes import session, request
from ProjectApp.entities import Librarian, Reader, Copy, Book
from datetime import datetime

# read = Reader('ofir@mail', 'ofir', 12345, 'Tel Aviv', 12344, datetime.now())
# if read:
#     print('if-able and true')
# else:
#     print('if-able and false')
test = 'Harry Potter And The Philosophers Stone'
cursor.execute('SELECT * FROM Book WHERE book_name LIKE %s', test.lower())
book = cursor.fetchone()
print(book)