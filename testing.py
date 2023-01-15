from ProjectApp import connection, cursor
from ProjectApp.routes import session, request, flash
from ProjectApp.entities import Librarian, Reader, Copy, Book
from datetime import datetime, date, timedelta

reader_demo = Reader('read@mail.com', 'ofir brand', 123445, 'Tel Aviv', 1111, datetime.now().date())
librarian_demo = Librarian('ofir@mail.com', 'ofir brand', 123445, 'Tel Aviv', 1111, datetime.now().date(),
                           'Ramat Aviv')


print(reader_demo.my_orders())