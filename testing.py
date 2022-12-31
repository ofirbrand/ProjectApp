from ProjectApp import connection, cursor
from ProjectApp.routes import session, request
from ProjectApp.entities import Librarian, Reader

# city, street, house_number

cursor.execute("SELECT * FROM Librarian_Address")
address = cursor.fetchone()
print(address)
email = 'ofirbrand@gmail.com'
password = "1234"
cursor.execute("SELECT * FROM Reader WHERE reader_email = %s", email)
reader_temp = cursor.fetchone()
cursor.execute("SELECT * FROM Librarian WHERE librarian_email = %s", email)
librarian_temp = cursor.fetchone()
print(reader_temp)
print(librarian_temp)
if reader_temp:
    print("the current user is a Reader")
    if reader_temp[3] == password:
        cursor.execute("SELECT city, street, house_number FROM Reader_Address WHERE reader_email = %s", email)
        address = cursor.fetchone()
        session = Reader(email=reader_temp[1], name=reader_temp[2], phone_num=reader_temp[0],
                         address=address, password=reader_temp[3], d_birth=reader_temp[4])
        print(f"The Reader which connect is {session.name}")
elif librarian_temp:
    print("the current user is a Librarian")
    if librarian_temp[3] == password:
        cursor.execute("SELECT city, street, house_number FROM Librarian_Address WHERE librarian_email = %s", email)
        address = cursor.fetchone()
        session = Librarian(email=librarian_temp[1], name=librarian_temp[2], phone_num=librarian_temp[0],
                            address=address, password=librarian_temp[3], work_date_begin=librarian_temp[4],
                            branch_name=librarian_temp[5])
        print(f"The Librarian which connect is {session.name}")
else:
    print('Password Incorrect')
# email, name, phone_num, address, password, work_date_begin, branch_name
keys = list(session.__dict__.keys())
values = list(session.__dict__.values())
for key, value in session.__dict__.items():
    print(key + " :" + str(value))
