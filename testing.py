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
request_id = 4
cursor.execute("""SELECT C.amount, C.copy_status, C.copy_id, BOR.reader_email, BOR.returned_date
                            FROM Borrow AS Bor, Copies AS C 
                            WHERE Bor.copy_id = C.copy_id
                            AND Bor.request_id = %s;""", request_id)
temp_request = cursor.fetchone()
if temp_request[0] > 0 and temp_request[1] == "available":
    print(temp_request)
else:
    print("you fucking idiot")

# def return_book(request_id):
#     cursor.execute("SELECT * FROM Order_Book WHERE request_id = %s", request_id)
#     is_order = cursor.fetchone()
#     if is_order:
#         cursor.execute("SELECT B.book_id, C.copy_id, C.amount "
#                        "FROM Book as B, Borrow AS BOR, Copies AS C "
#                        "WHERE B.book_id = C.book_id "
#                        "AND C.copy_id = BOR.copy_id "
#                        "AND BOR.request_id = %s", request_id)
#         current_request = cursor.fetchone()
#         cursor.execute("UPDATE Order_book SET order_status = 'waiting' AND returned_date = %s "
#                        "WHERE request_id = %s", (request_id, datetime.now().date()))
#         cursor.execute("UPDATE Copies SET copy_status = 'available' WHERE copy_id = %s", current_request[1])
#         cursor.execute("UPDATE Copies SET amount = %s WHERE book_id = %s",
#                        (int(int(current_request[2]) + 1), current_request[0]))
#         cursor.execute("UPDATE Borrow SET returned_date = %s AND status_of_request = 'returned' WHERE request_id = %s",
#                        (datetime.now().date(), request_id))
#         connection.commit()
#         return flash("The Book Has Been Successfully Returned", 'success')
#     else:
#         cursor.execute("SELECT B.book_id, C.copy_id, C.amount "
#                        "FROM Book as B, Borrow AS BOR, Copies AS C "
#                        "WHERE B.book_id = C.book_id "
#                        "AND C.copy_id = BOR.copy_id "
#                        "AND BOR.request_id = %s", request_id)
#         current_request = cursor.fetchone()
#         cursor.execute("UPDATE Copies SET copy_status = 'available' WHERE copy_id = %s", current_request[1])
#         cursor.execute("UPDATE Copies SET amount = %s WHERE book_id = %s",
#                        (int(int(current_request[2]) + 1), current_request[0]))
#         cursor.execute("UPDATE Borrow SET returned_date = %s AND status_of_request = 'returned' WHERE request_id = %s",
#                        (datetime.now().date(), request_id))
#         connection.commit()
#         return flash("The Book Has Been Successfully Returned", 'success')
#
