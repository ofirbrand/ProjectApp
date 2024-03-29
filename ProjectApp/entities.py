from datetime import datetime, timedelta, date
from ProjectApp.routes import flash
from ProjectApp import cursor, connection


class User:  # reader and librarian classes inherit from user classs
    counter = 0

    def __init__(self, email, name, phone_num, address, password):
        self.email = email
        self.name = name
        self.phone_num = phone_num
        self.address = address
        self.password = password
        User.counter += 1


class Librarian(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, password, work_date_begin, branch_name):
        super().__init__(email, name, phone_num, address, password)
        self.work_date_begin = work_date_begin
        self.branch_name = branch_name
        self.user_type = "Librarian"
        Librarian.counter += 1

    # add new book function
    def add_new_book(self, book):
        cursor.execute("SELECT * FROM Book WHERE book_name like %s and author like %s;",
                       (book.book_name, book.author))
        is_book = cursor.fetchone()
        if is_book:  # check if the book already exists
            cursor.execute("SELECT * FROM Copies WHERE Book_id = %s and branch_name = %s;",
                           (book.book_id, self.branch_name))
            is_copy = cursor.fetchone()
            if is_copy:  # check if the copy that exists is in the same branch
                cursor.execute(""" SELECT C.copy_id, C.book_id, B.book_name, B.author, B.publisher, B.publish_year, 
                                            C.branch_name, C.amount
                                            FROM Copies AS C JOIN Book AS B ON C.book_id = B.book_id
                                            WHERE C.branch_name = %s AND C.book_id = %s""", (is_copy[2], is_copy[1]))
                copy_catch = cursor.fetchone()
                copy_temp = Copy(copy_id=copy_catch[0], book_id=copy_catch[1], book_name=copy_catch[2],
                                 author=copy_catch[3], publisher=copy_catch[4], year_published=copy_catch[5],
                                 branch=copy_catch[6], amount=copy_catch[7])
                copy_temp.add_copy()
                copy_temp.update_exist_copy()  # add 1 amount to all the copies with this book-id and branch-name
                return
            else:  # The book isn't exists in this branch. add new copy
                cursor.execute("INSERT INTO Copies(book_id, branch_name,amount, copy_status) VALUES(%s, %s, %s, %s)",
                               (book.book_id, self.branch_name, int(1), str('available')))
                connection.commit()
                return flash("A New Copy Has Been Added", 'success')
        else:  # the book isn't exists, add new book and new copy
            # add new book to the database
            cursor.execute("INSERT INTO Book(book_id, book_name, author, publisher, publish_year) "
                           "VALUES(%s, %s, %s, %s, %s)",
                           (book.book_id, book.book_name, book.author, book.publisher, book.year_published))
            connection.commit()
            # add new copy to the database
            cursor.execute("INSERT INTO Copies(book_id, branch_name, amount, copy_status) VALUES(%s, %s, %s, %s)",
                           (book.book_id, self.branch_name, int(1), str('available')))
            connection.commit()
            return flash(f"{book.book_name} Created As A New Book", 'success')

    # show all the relevant requests for each librarian (for books from his branch)
    def show_requests(self):
        cursor.execute("""SELECT C.copy_id, Book.book_name, C.amount, C.copy_status, Bor.request_id, 
                          Bor.reader_email, Bor.status_of_request 
                          FROM Borrow AS Bor, Copies AS C, Book
                          WHERE Bor.copy_id = C.copy_id
                          AND Book.book_id = C.book_id
                          AND Bor.status_of_request  = 'requested'
                          AND C.branch_name = %s""", self.branch_name)
        requests_catch = cursor.fetchall()
        requests_caught = list(map(list, requests_catch))
        requests = []
        for request in requests_caught:  # this loop check if there is an order for every branch
            lst = list(request)
            cursor.execute("SELECT order_status, reader_email FROM Order_book WHERE copy_id = %s", request[0])
            order_catch = cursor.fetchall()
            if order_catch:
                orders = list(map(list, order_catch))
                for order in orders:  # check if the order made by the same person who ask to borrow this copy
                    if order[0] == str('waiting'):
                        if request[5] == order[1]:
                            order_status = 'orderable'
                            lst.append(order_status)
                        else:
                            order_status = 'waiting'
                            lst.append(order_status)
                    else:
                        order_status = 'orderable'
                        lst.append(order_status)
            else:
                order_status = 'orderable'
                lst.append(order_status)
            requests.append(lst)
        return requests

    # function that deals with all the borrow requests - both decline or approve buttons direct to this function
    def manage_request(self, request_id):
        cursor.execute("""SELECT C.amount, C.copy_status, C.copy_id, Bor.reader_email, Bor.returned_date, 
                                C.branch_name, C.book_id
                            FROM Borrow AS Bor, Copies AS C 
                            WHERE Bor.copy_id = C.copy_id
                            AND Bor.request_id = %s;""", request_id)
        temp_request = cursor.fetchone()
        # check if the borrower already have more than 3 books
        cursor.execute("""SELECT * FROM Borrow 
                            WHERE reader_email = %s AND status_of_request = 'approved' """, temp_request[3])
        current_holding_books = cursor.fetchall()
        if len(current_holding_books) > 2:  # deny this request
            cursor.execute("UPDATE Borrow SET status_of_request = 'denied' WHERE request_id = %s", request_id)
            connection.commit()
            return flash('The Borrow request was rejected because the reader already hold 3 books', 'danger')
        else:
            # check if the copy_status is available and amount in stock > 0
            if temp_request[0] > 0 and temp_request[1] == "available":
                # check if there is an order for this copy
                cursor.execute("SELECT * FROM Order_book WHERE copy_id = %s", temp_request[2])
                orders_catch = cursor.fetchall()
                today = datetime.now().date()
                return_date = today + timedelta(days=14)
                if orders_catch:
                    orders = list(map(list, orders_catch))
                    for order in orders:
                        if order[3] != 'waiting':
                            # update: copy_amount, copy_status, borrow_status, borrow_date, return_date to default + 14
                            cursor.execute("UPDATE Copies SET amount = amount - 1 "
                                           "WHERE book_id = %s AND branch_name = %s",
                                           (temp_request[6], temp_request[5]))
                            connection.commit()
                            cursor.execute("UPDATE Copies SET copy_status = 'orderable' WHERE Copy_id = %s",
                                           temp_request[2])
                            connection.commit()
                            cursor.execute("UPDATE Borrow "
                                           "SET status_of_request = 'approved', date_of_borrowing = %s, returned_date = %s "
                                           "WHERE request_id = %s", (today, return_date, request_id))
                            connection.commit()
                            return flash('Borrow Request Successfully Approved', 'success')
                        else:
                            if (today - order[4]).days < 3:  # check if there is open order
                                if temp_request[3] == order[2]:  # this situation is the execution of order request
                                    # update: copy_amount, copy_status, borrow_status, borrow_date, order_status
                                    cursor.execute("UPDATE Copies SET amount = amount - 1 "
                                                   "WHERE book_id = %s AND branch_name = %s",
                                                   (temp_request[6], temp_request[5]))
                                    connection.commit()
                                    cursor.execute("UPDATE Copies SET copy_status = 'orderable' WHERE Copy_id = %s",
                                                   temp_request[2])
                                    connection.commit()
                                    cursor.execute("UPDATE Borrow "
                                                   "SET status_of_request = 'approved', date_of_borrowing = %s, returned_date = %s "
                                                   "WHERE request_id = %s", (today, return_date, request_id))
                                    connection.commit()
                                    cursor.execute("""UPDATE Order_book SET order_status = 'orderable' 
                                                   WHERE copy_id = %s, reader_email = %s, request_id = %s; """,
                                                   (order[0], order[2], order[1]))
                                    connection.commit()
                                    return flash('Borrow Request Successfully Approved', 'success')
                                else:  # update status of request to denied
                                    cursor.execute("UPDATE Borrow SET status_of_request = 'denied' "
                                                   "WHERE request_id = %s", request_id)
                                    connection.commit()
                                    return flash("The Borrow request was rejected because the book is reserved", 'danger')
                            else:
                                # update: copy_amount, copy_status, borrow_status, borrow_date, order_status
                                cursor.execute("UPDATE Copies SET amount = amount - 1 "
                                               "WHERE boo_id = %s AND branch_name = %s",
                                               (temp_request[6], temp_request[5]))
                                connection.commit()
                                cursor.execute("UPDATE Copies SET copy_status = 'orderable' WHERE Copy_id = %s",
                                               temp_request[2])
                                connection.commit()
                                cursor.execute("UPDATE Borrow SET status_of_request = 'approved', "
                                               "date_of_borrowing = %s, returned_date = %s WHERE request_id = %s",
                                               (today, request_id, return_date))
                                connection.commit()
                                cursor.execute("UPDATE Order_book SET order_status = 'orderable' "
                                               "WHERE copy_id = %s AND reader_email = %s AND request_id = %s",
                                               (order[3], order[2], order[1]))
                                connection.commit()
                                return flash('Borrow Request Successfully Approved', 'success')
                else:
                    # update: copy_amount, copy_status, borrow_status, borrow_date
                    cursor.execute("UPDATE Copies SET amount = amount - 1 WHERE book_id = %s AND branch_name = %s",
                                   (temp_request[6], temp_request[5]))
                    connection.commit()
                    cursor.execute("UPDATE Copies SET copy_status = 'orderable' WHERE Copy_id = %s",
                                   temp_request[2])
                    connection.commit()
                    cursor.execute("UPDATE Borrow SET status_of_request = 'approved', date_of_borrowing = %s, "
                                   "returned_date = %s WHERE request_id = %s", (today, return_date, request_id))
                    connection.commit()
                    return flash('Borrow Request Successfully Approved', 'success')
            else:
                cursor.execute("UPDATE Borrow SET status_of_request = 'denied' WHERE request_id = %s", request_id)
                connection.commit()
                return flash("The Borrow request was rejected because the book isn't available", 'danger')


class Reader(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, password, d_birth):
        super().__init__(email, name, phone_num, address, password)
        self.d_birth = d_birth
        self.user_type = "Reader"
        Reader.counter += 1

    # search function from reader homepage
    def search_book(self, word):  # book[7] is the copy id with the smallest value from the same book.id in this branch
        word = "%" + word + "%"  # to search if this word is part of book or author name
        cursor.execute("SELECT book_name FROM Book WHERE book_name LIKE %s", word)
        is_book_exist = cursor.fetchall()
        cursor.execute("SELECT author FROM Book WHERE author LIKE %s", word)
        is_author_exist = cursor.fetchall()
        if is_author_exist:  # search by author name
            authors = [''.join(i) for i in is_author_exist]
            books_list = []
            for author in authors:
                cursor.execute("""SELECT B.book_name, B.author, C.branch_name, MAX(C.amount), BR.phone_number, 
                                SUM(CASE WHEN C.copy_status LIKE 'available' THEN 1 ELSE 0 END),
                                SUM(CASE WHEN C.copy_status LIKE 'orderable' THEN 1 ELSE 0 END)
                                FROM Copies AS C, Book AS B, Branch as BR
                                WHERE C.book_id = B.book_id 
                                AND B.author LIKE %s 
                                AND BR.branch_name = C.branch_name 
                                GROUP BY 1 , 2 , 3""", author)
                # show orderable copies only when there are no available copies
                books_catch = cursor.fetchall()
                for b in books_catch:
                    lst = list(b)
                    books_list.append(lst)
            #new content to catch the copy_id
            for book in books_list:
                cursor.execute("""SELECT C.copy_id
                                    FROM Book AS B, Copies AS C
                                    WHERE B.book_id = C.book_id
                                    AND B.book_name = %s
                                    AND B.author = %s
                                    AND C.branch_name = %s""", (book[0], book[1], book[2]))
                copy_id = cursor.fetchone()
                book.append(copy_id[0])
            # end new content
            return books_list
        elif is_book_exist:  # search by author name
            books = [''.join(i) for i in is_book_exist]
            books_list = []
            for book in books:
                cursor.execute("""SELECT B.book_name, B.author, C.branch_name, MAX(C.amount), BR.phone_number, 
                                SUM(CASE WHEN C.copy_status LIKE 'available' THEN 1 ELSE 0 END),
                                SUM(CASE WHEN C.copy_status LIKE 'orderable' THEN 1 ELSE 0 END)
                                FROM Copies AS C, Book AS B, Branch as BR
                                WHERE C.book_id = B.book_id 
                                AND B.book_name LIKE %s 
                                AND BR.branch_name = C.branch_name
                                GROUP BY 1 , 2 , 3""", book)
                books_catch = cursor.fetchall()
                for b in books_catch:
                    lst = list(b)
                    books_list.append(lst)
            for book in books_list:
                cursor.execute("""SELECT C.copy_id
                                    FROM Book AS B, Copies AS C
                                    WHERE B.book_id = C.book_id
                                    AND B.book_name = %s
                                    AND B.author = %s
                                    AND C.branch_name = %s""", (book[0], book[1], book[2]))
                copy_id = cursor.fetchone()
                book.append(copy_id[0])
            return books_list
        else:  # the word isn't of any boor or author name
            return flash(f"No Book Or Author In The System Such As '{word[1:-1]}' ", 'danger')

    # borrow request - reader side (only send request for a specific copy)
    # wait for librarian answer for this request
    def borrow_request(self, copy_id):
        # check if the reader holds more than 3 books
        cursor.execute("SELECT count(request_id) "
                       "FROM Borrow "
                       "WHERE reader_email = %s"
                       "AND status_of_request = 'approved'", self.email)
        amount_of_books = cursor.fetchone()
        if amount_of_books[0] >= 3:
            return flash(f"Sorry {self.name}, You Already Have 3 Books And Reader Can Hold Up To 3 Books", 'danger')
        else:  # check if the wanted copy is available
            cursor.execute("SELECT copy_status FROM Copies WHERE copy_id = %s", copy_id)
            is_copy_available = cursor.fetchone()
            if is_copy_available[0] == 'available':
                cursor.execute("INSERT INTO Borrow (status_of_request, copy_id, reader_email)"
                               "VALUES (%s, %s, %s)",
                               ('requested', copy_id, self.email))
                connection.commit()
                return flash(f"Your Borrow Request has been Received And Waiting To Be Approved", 'success')
            else:
                return flash("This Book Isn't Available So It Cannot Be Borrowed", 'danger')

    # this function show my books: current holding, open requests and books history (returned books)
    def my_books(self):
        cursor.execute("""SELECT Book.book_name, Book.author, C.copy_id, C.branch_name, Bor.date_of_borrowing ,
                            Bor.request_id, Bor.status_of_request, Bor.returned_date
                            FROM Reader as R, Borrow as Bor, Copies as C, Book
                            WHERE R.reader_email = Bor.reader_email
                            AND Bor.copy_id = C.copy_id
                            AND C.book_id = Book.book_id
                            AND Bor.reader_email = %s ;""", self.email)
        books_caught = cursor.fetchall()
        if books_caught:
            my_books = list(map(list, books_caught))
            for book in my_books:  # this loop enters the expected return date for each book
                if book[4]:
                    return_date = book[4] + timedelta(days=14)
                    book.append(return_date)
                else:
                    return_date = None
                    book.append(return_date)
            return my_books
        else:
            return flash(f"{self.name}, You Currently Don't Hold Any Book, Don't Have Any Open Requests Or Borrow "
                         f"History", 'danger')

    # this function show my orders - to my books page
    def my_orders(self):  # check if there are any orders for this reader to show in my books
        cursor.execute("""SELECT Book.book_name, B.returned_date, B.copy_id, O.reader_email, O.order_status, Book.book_id  
                            FROM Borrow AS B, Order_book AS O, Copies AS C, Book
                            WHERE B.request_id = O.request_id
                            AND B.copy_id = C.copy_id 
                            AND C.book_id = Book.book_id
                            AND O.reader_email = %s;""", self.email)
        catch_orders = cursor.fetchall()
        if catch_orders:  # check if the reader have any open orders
            orders = list(map(list, catch_orders))
            # print(orders)
            for order in orders:  # check if the order is still relevant
                if order[4] == 'orderable':  # check if the order status is orderable
                    show_order = 'no'
                    order.append(show_order)
                elif order[4] == 'waiting':  # check if the order status is waiting
                    today = datetime.now().date()
                    if (today - order[1]).days < 3:  # check if the order wait more than 3 days
                        show_order = 'yes'
                        order.append(show_order)
                    else:
                        show_order = 'no'
                        order.append(show_order)
                else:
                    show_order = 'yes'
                    order.append(show_order)
                # check if this reader already asks to borrow this book (after he ordered it)
                cursor.execute("""SELECT B.status_of_request, B.returned_date
                                    FROM Borrow AS B, Copies AS C
                                    WHERE C.copy_id = B.copy_id AND B.reader_email = %s AND C.book_id = %s;""",
                               (order[3], order[5]))
                other_requests = cursor.fetchall()
                if other_requests:
                    requests = list(map(list, other_requests))
                    requests_status = []
                    for request in requests:  # this loop check what is the status of the other requests of this user
                        if request[0] == "requested":
                            stat = 'requested'
                            requests_status.append(stat)
                        else:
                            stat = 'not requested'
                            requests_status.append(stat)
                    if "requested" in requests_status:
                        order.append('no show')
                    else:
                        order.append('show')
                else:
                    order.append('show')
            # print(requests_status)
            return orders
        else:
            return None

    def extension(self, request_id):
        today = datetime.now().date()
        cursor.execute("SELECT * FROM Borrow WHERE request_id = %s", request_id)
        request_catch = cursor.fetchone()
        # check if the expected return date has expired
        if (request_catch[5] - today).days <= 0:
            return flash("The book return date has passed! "
                         "An extension cannot be requested and the book must be returned as soon as possible", 'danger')
        else:
            # check if the book has been ordered
            cursor.execute("SELECT order_status FROM Order_book WHERE copy_id = %s", request_catch[3])
            order_catch = cursor.fetchall()
            if order_catch:
                orders = list(map(list, order_catch))
                is_ordered = []
                for order in orders:  # loop over the orders for this copy_id to check their order status
                    if order[0] == 'ordered':  # the book is ordered
                        is_ordered.append('ordered')
                    else:  # the book isn't ordered
                        is_ordered.append('not-ordered')
                if str('ordered') in is_ordered:
                    return flash("It Is Not Possible To Extend The Borrow Period Due To The Book Being Ordered "
                                 "By Another Reader", 'danger')
                else:
                    cursor.execute("SELECT returned_date FROM Borrow WHERE request_id = %s", request_id)
                    current_date_of_return = cursor.fetchone()
                    new_returned_date = current_date_of_return[0] + timedelta(days=7)
                    cursor.execute("UPDATE Borrow SET (returned_date = %s, extension_date = %s) WHERE request_id = %s",
                                   (new_returned_date, today, request_id))
                    connection.commit()
                    return flash('Your Request For An Extension Has Been Accepted', 'success')
            else:
                cursor.execute("SELECT returned_date FROM Borrow WHERE request_id = %s", request_id)
                current_date_of_return = cursor.fetchone()
                new_returned_date = current_date_of_return[0] + timedelta(days=7)
                cursor.execute("UPDATE Borrow SET returned_date = %s, extension_date = %s WHERE request_id = %s ",
                               (new_returned_date, today, request_id))
                connection.commit()
                return flash('Your Request For An Extension Has Been Accepted', 'success')

    # order book function
    def order_book(self, copy_id, reader_email):
        # check who Borrowed this book - if it's the reader who trying to order it, deny the order request
        cursor.execute("""SELECT reader_email FROM Borrow 
                            WHERE copy_id = %s
                            AND (status_of_request = 'approved' or status_of_request = 'expired')""", copy_id)
        borrower_email = cursor.fetchone()
        if borrower_email[0] == reader_email:  # you Have This book so you cannot order it
            return flash("Your Have This Book. You Cannot Order A Book That You Already Have", 'danger')
        else:
            # check if there are any orders for this copy
            cursor.execute("SELECT order_status, request_id, reader_email FROM Order_book WHERE copy_id = %s", copy_id)
            orders_catch = cursor.fetchall()
            # if this book already been ordered before, check if the order is valid
            if orders_catch:
                orders = list(map(list, orders_catch))
                # is_order_valid = []
                for order in orders:
                    if order[0] != 'orderable':
                        # is_order_valid.append('ordered')
                        return flash("Sorry, The Book Cannot Be Ordered Because It Has Already Been "
                                     "Ordered By Another Reader", 'danger')
            #     # means the order isn't valid
            #     # Update the copy status to "orderable"
            #     cursor.execute("UPDATE Copies SET copy_status = 'not-orderable' "
            #                    "WHERE request_id = %s AND reader_email = %s", (order[1], order[2]))
            #     # create new order
            #     cursor.execute("INSERT INTO Order_book "
            #                    "(copy_id, request_id, reader_email, order status, order_date)"
            #                    "VALUES (%s, %s, %s, %s, %s)",
            #                    (copy_id, order[1], reader_email, 'ordered', datetime.now().date()))
            #     connection.commit()
            #     return flash("Your Order Request Has Been Approved. The Book Will Be Available For Pickup Soon",
            #                  'success')
            # else:
            # there is no order for this copy - create new one
            cursor.execute("""SELECT request_id 
                                FROM Copies as C JOIN Borrow AS B ON C.copy_id = B.copy_id
                                WHERE B.copy_id = %s 
                                AND (B.status_of_request = 'approved' or B.status_of_request = 'expired') 
                                AND C.copy_status = 'orderable' """, copy_id)
            request_catch = cursor.fetchone()
            # Update the order status to "ordered"
            cursor.execute("INSERT INTO Order_book (copy_id, request_id, reader_email, order_status, order_date) "
                           "VALUES(%s, %s, %s, %s, %s)",
                           (copy_id, request_catch[0], reader_email, 'ordered', datetime.now().date()))
            connection.commit()
            cursor.execute("UPDATE Copies SET copy_status = 'not-orderable' WHERE copy_id = %s", copy_id)
            connection.commit()
            return flash("Your Order Request Has Been Approved. The Book Will Be Available For Pickup Soon",
                         'success')

    def return_book(self, copy_id, request_id):
        # check if this book has been ordered - to change his order status so the user who ordered it will be up-to-date
        cursor.execute("SELECT * FROM Order_book WHERE copy_id = %s", copy_id)
        is_order = cursor.fetchone()
        if is_order:  # if it ordered
            cursor.execute("SELECT B.book_id, C.copy_id, C.amount, C.branch_name "
                           "FROM Book as B, Borrow AS BOR, Copies AS C "
                           "WHERE B.book_id = C.book_id "
                           "AND C.copy_id = BOR.copy_id "
                           "AND BOR.request_id = %s", request_id)
            current_request = cursor.fetchone()  # set order status to 'waiting'
            cursor.execute("UPDATE Order_book SET order_status = 'waiting', returned_date = %s "
                           "WHERE request_id = %s", (datetime.now().date(), request_id))
            cursor.execute("UPDATE Copies SET copy_status = 'available' "
                           "WHERE book_id = %s AND branch_name = %s ", (current_request[0], current_request[3]))
            cursor.execute("UPDATE Copies SET amount = amount + 1 WHERE book_id = %s",
                           current_request[0])
            cursor.execute("UPDATE Borrow SET returned_date = %s, status_of_request = 'returned' WHERE request_id = %s",
                           (datetime.now().date(), request_id))
            connection.commit()
            return flash("The Book Has Been Successfully Returned", 'success')
        else:
            cursor.execute("SELECT B.book_id, C.copy_id, C.amount. C.branch_name "
                           "FROM Book as B, Borrow AS BOR, Copies AS C "
                           "WHERE B.book_id = C.book_id "
                           "AND C.copy_id = BOR.copy_id "
                           "AND BOR.request_id = %s", request_id)
            current_request = cursor.fetchone()
            cursor.execute("UPDATE Copies SET copy_status = 'available' WHERE copy_id = %s", current_request[1])
            cursor.execute("UPDATE Copies SET amount = %s WHERE book_id = %s AND branch_name = %s",
                           (int(int(current_request[2]) + 1), current_request[0], current_request[3]))
            cursor.execute("UPDATE Borrow SET returned_date = %s, status_of_request = 'returned' "
                           "WHERE request_id = %s", (datetime.now().date(), request_id))
            connection.commit()
            return flash("The Book Has Been Successfully Returned", 'success')

class Book:
    counter = 0

    def __init__(self, book_id, book_name, author, year_published, publisher):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.year_published = year_published
        self.publisher = publisher
        Book.counter += 1


class Copy(Book):
    def __init__(self, copy_id, book_id, book_name, author, year_published, publisher, branch, amount):
        super(Copy, self).__init__(book_id, book_name, author, year_published, publisher)
        self.copy_id = copy_id
        self.branch = branch
        self.status = 'available'
        self.amount = amount

    def add_copy(self):
        cursor.execute("INSERT INTO Copies(book_id, branch_name, copy_status, amount) VALUES(%s, %s, %s, %s)",
                       (self.book_id, self.branch, self.status, self.amount))
        connection.commit()
        # return flash('A New Copy Has Been Added', 'success')
        return flash("A New Copy Has Been Added", 'success')

    def update_exist_copy(self):
        cursor.execute("UPDATE Copies SET amount = %s WHERE book_id = %s AND branch_name = %s",
                       ((int(self.amount) + 1), self.book_id, self.branch))
        connection.commit()
        # return flash('This Book Is Already Exist. A New Copy Has Been Added', 'success')
        return flash("A New Copy Has Been Added And Copies Are Up To Date", 'success')






