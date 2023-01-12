from ProjectApp import connection, cursor
from ProjectApp.routes import session, request, flash
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

# books = reader_demo.my_books()
# # my_books = list(map(list, books))
# print(books[0])

# cursor.execute("SELECT * FROM Borrow")
# current_request = cursor.fetchone()
# print(current_request)
request_id = 2
# cursor.execute("""SELECT C.amount, C.copy_status, C.copy_id, BOR.reader_email, BOR.returned_date
#                             FROM Borrow AS Bor, Copies AS C
#                             WHERE Bor.copy_id = C.copy_id
#                             AND Bor.request_id = %s;""", request_id)
# temp_request = cursor.fetchone()
# if temp_request[0] > 0 and temp_request[1] == "available":
#     print(temp_request)
# else:
#     print("you fucking idiot")

# today = datetime.now().date()
# another_date = date(year=2023, month=2, day=3)
# print((another_date - today).days)

copy_id = 2

def show_orders(email):
    cursor.execute("""SELECT Book.book_name, B.returned_date 
                        FROM Borrow AS B, Order_book AS O, Copies AS C, Book
                        WHERE B.request_id = O.request_id
                        AND B.copy_id = C.copy_id 
                        AND C.book_id = Book.book_id
                        AND O.reader_email = %s;""", email)
                        # change email to self.email
    catch_orders = cursor.fetchall()
    if catch_orders:
        orders = list(map(list, catch_orders))
        return orders
    else:
        print('No orders for this you')
email = reader_demo.email
# print(show_orders(email))

orders = reader_demo.my_orders()
today = datetime.now().date()
if orders:
    three_days = timedelta(days=3)
    for order in orders:
        print((order[1] + three_days))