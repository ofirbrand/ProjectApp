from ProjectApp import connection, cursor
from ProjectApp.routes import session, request
from ProjectApp.entities import Librarian, Reader, Copy, Book
from datetime import datetime

search_word = "dani"
search_word = "%" + search_word + "%"
cursor.execute("SELECT book_name FROM Book WHERE book_name LIKE %s", search_word)
is_book_exist = cursor.fetchall()
cursor.execute("SELECT author FROM Book WHERE author LIKE %s", search_word)
is_author_exist = cursor.fetchall()
if is_author_exist:
    authors = [''.join(i) for i in is_author_exist]
    books_list = []
    for author in authors:
        cursor.execute("""SELECT B.book_name, B.author, C.branch_name, MAX(C.amount),
                        SUM(CASE WHEN C.copy_status LIKE 'available' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN C.copy_status LIKE 'orderable' THEN 1 ELSE 0 END)
                        FROM Copies AS C JOIN Book AS B ON C.book_id = B.book_id
                        WHERE B.author LIKE %s
                        GROUP BY 1 , 2 , 3""", author)
        books_catch = cursor.fetchall()
        for b in books_catch:
            lst = list(b)
            books_list.append(lst)
    for book in books_list:
        print(book)
elif is_book_exist:
    books = [''.join(i) for i in is_book_exist]
    books_list = []
    for book in books:
        cursor.execute("""SELECT B.book_name, B.author, C.branch_name, MAX(C.amount),
                        SUM(CASE WHEN C.copy_status LIKE 'available' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN C.copy_status LIKE 'orderable' THEN 1 ELSE 0 END)
                        FROM Copies AS C JOIN Book AS B ON C.book_id = B.book_id
                        WHERE B.book_name LIKE %s
                        GROUP BY 1 , 2 , 3""", book)
        books_catch = cursor.fetchall()
        for b in books_catch:
            lst = list(b)
            books_list.append(lst)
    for book in books_list:
        print(book)
else:
    print(f"No Book Or Author In The System Such As {search_word}")

### my books query:
"""
select Book.book_name, C.copy_id, C.branch_name,Bor.date_of_borrowing ,Bor.request_id
from Reader as R, Borrow_Extension as Bor, Copies as C, Book
where R.reader_email = Bor.reader_email
and Bor.copy_id = C.copy_id
and C.book_id = Book.book_id
and Bor.status_of_request = 'borrowed';
"""