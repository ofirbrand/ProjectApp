from ProjectApp import connection, cursor
from ProjectApp.routes import session, request, flash
from ProjectApp.entities import Librarian, Reader, Copy, Book
from datetime import datetime, date, timedelta

reader = Reader('ofir@gmail.com', 'Ofir Brand', 526738977, 'address', 1111, '1995-12-02')
books = list(map(list, reader.search_book('har')))
for book in books:
    print(book)


