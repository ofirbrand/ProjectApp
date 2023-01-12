from ProjectApp import connection, cursor
from ProjectApp.routes import session, request
from ProjectApp.entities import Librarian, Reader, Copy, Book
from datetime import datetime, date, timedelta

reader_demo = Reader('read@mail.com', 'ofir brand', 123445, 'Tel Aviv', 1111, datetime.now().date())
librarian_demo = Librarian('ofir@mail.com', 'ofir brand', 123445, 'Tel Aviv', 1111, datetime.now().date(),
                           'City Center')
# print(librarian_demo.show_requests())
# print(librarian_demo.show_requests())
# a = datetime.now().date()
# a1 = date(year=a.year, month=a.month, day=a.day)
# b = date(year=2023, month=1, day=2)
# c = a1-b
# # a = a + 3
# print(a)
# print(b)
# print(c)
# # tuple_test = (('t', 'word'), ('second', 'test'))
# # new_test = list(map(list, tuple_test))
# # print(new_test)

books = reader_demo.my_books()
# my_books = list(map(list, books))
print(books[0])
# for book in books:
#     print(book)





# today = datetime.now().date()
# return_date = today + timedelta(days=14)
# print((return_date - today).days)
# cursor.execute("""SELECT Book.book_name, C.copy_id, C.branch_name, Bor.date_of_borrowing,
#                     Bor.request_id, Bor.status_of_request
#                     FROM Reader as R, Borrow as Bor, Copies as C, Book
#                     WHERE R.reader_email = Bor.reader_email
#                     AND Bor.copy_id = C.copy_id
#                     AND C.book_id = Book.book_id
#                     AND Bor.reader_email = %s ;""", reader_demo.email)
# books_caught = cursor.fetchall()
# my_books = list(map(list, books_caught))
# for book in my_books:
#     print(book)
### my current books query:
# """
# select Book.book_name, C.copy_id, C.branch_name, Bor.date_of_borrowing ,Bor.request_id
# from Reader as R, Borrow_Extension as Bor, Copies as C, Book
# where R.reader_email = Bor.reader_email
# and Bor.copy_id = C.copy_id
# and C.book_id = Book.book_id
# and Bor.status_of_request = 'borrowed';
# """

### my books history
# """SELECT Book.book_name, C.amount, C.copy_status
#     FROM Borrow AS Bor, Copies AS C, Book
#     WHERE Bor.book_id = C.book_id
#     AND Book.book_id = C.book_id
#     AND C.branch_name = 'Ramat Aviv'
#     AND Bor.request_id = 1;
# """
### Borrow_show
# need to add connect to the database
