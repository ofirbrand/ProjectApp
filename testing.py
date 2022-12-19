from datetime import datetime
from ProjectApp.entities import Borrow, Book, Librarian, Reader

a = datetime.now()
print(a.date())

librarian1 = Librarian('ofir@mail.com', 'ofir', 1223, 'Tel-Aviv', 1234, datetime.now().date(), 'Great Branch')
reader1 = Reader('doron@email.com', 'doron', 1122, 'Lod', 1111, '1995')
