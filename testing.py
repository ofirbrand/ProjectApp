from ProjectApp import connection, cursor
from ProjectApp.routes import session, request
from ProjectApp.entities import Librarian,  Reader
cursor.execute("SELECT city, street, house_number FROM Librarian_Address")
address = cursor.fetchone()
print(address)
email = 'ofirbrand@gmail.com'
password = '1234'
cursor.execute("SELECT * FROM Reader WHERE reader_email = %s", email)
reader_temp = cursor.fetchone()
cursor.execute("SELECT * FROM Librarian WHERE librarian_email = %s", email)
librarian_temp = cursor.fetchone()
print(reader_temp)
print(librarian_temp)
if reader_temp:
    if reader_temp[3] == password:
        cursor.execute("SELECT city, street, house_number FROM Reader_Address WHERE email reader_email = %s", email)
        address = cursor.fetchone()
        session = Reader(email=reader_temp[1], name=reader_temp[2], phone_num=reader_temp[0],
                         address=address, password=reader_temp[3], d_birth=reader_temp[4])
        f"The Reader which connect is {session.name}"
    else:
        print('Password Incorrect')
# elif librarian_temp:
#     if librarian_temp[3] == password:
#         session["email"] = request.form.get("email")
#         redirect('/reader')
#     else:
#         print('Password Incorrect', 'error')
# else:
#     print('The Email Address Is Not Saved In The System. Sign-Up Or Check For A Typo')
#     redirect('/')