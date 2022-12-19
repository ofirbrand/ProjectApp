import re
from datetime import datetime
#No need for argument testing inside the classes - it will be testing during the form building/testing
#User arguments (common for Librarian's and Reader's) - email, name, phone_num, address
#No need for using @property and @setter
class User:
    counter = 0

    def __init__(self, email, name, phone_num, address):
        self.__email = email
        self.__name = name
        self.__phone_num = phone_num
        self.__address = address
        User.counter += 1

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        # add test that check if the email address is correct
        set1 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(set1, email):
            self.__email = email
        else:
            raise TypeError("Please insert valid email address. for example: try_this@example.cpm")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) == str:
            self.__name = name
        else:
            raise TypeError("users first name must be a string")

    @property
    def phone_num(self):
        return self.__phone_num

    @phone_num.setter
    def phone_num(self, num):
        # add test that check if the date is correct
        if type(num) == int and 4 < len(num) < 15:
            self.__phone_num = num
        else:
            raise TypeError("Please insert valid phone number")

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        # add test that check if the address is correct
        if len(address) == 3 and type(address[0]) == str and type(address[1]) == str and type(address[2]) == int:
            self.__address = address
        else:
            raise TypeError("Please insert valid address such as: city(word), street name(word), house number(number)")

    def __str__(self):
        str1 = f'Users name is: {self.__name}'
        return str1

#inherit basic argument from User class
#Librarian's unique arguments = work_date_begin, branch
###create tests for email, work_date_begin(valid date argument)
class Librarian(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, work_date_begin, branch):
        super().__init__(email, name, phone_num, address)
        self.__work_date_begin = work_date_begin
        self.__branch = branch
        Librarian.counter += 1

    @property
    def work_date_begin(self):
        return self.__work_date_begin

    # create test to valid date
    @work_date_begin.setter
    def work_date_begin(self, date):
        #add test that check if the date is correct
        if type(date) == str:
            self.work_date_begin = date
        else:
            raise TypeError("Please insert valid date such as YYYY-MM-DD")

    @property
    def branch(self):
        return self.__branch

    #check if the branch test is good enough
    @branch.setter
    def branch(self, branch):
        # add test that check if the email address is correct
        if type(branch) == str:
            self.__branch = branch
        else:
            raise TypeError("branch name must be a word")

#inherit basic argument from User class
#Reader's arguments - email, name, d_birth, phone_num, address
#build valid date test for d_birth
class Reader(User):
    counter = 0

    def __init__(self, email, name, phone_num, address, d_birth):
        super().__init__(email, name, phone_num, address)
        self.__d_birth = d_birth
        Reader.counter += 1

    @property
    def d_birth(self):
        return self.__d_birth

    @d_birth.setter
    def d_birth(self, date):
        try:
            if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            is_valid = True
        except ValueError:
            is_valid = False
        if is_valid:
            self.__d_birth = date
        else:
            raise ValueError("Date argument must be in the template of yyyy-mm-dd")


class Book:
    counter = 0

    def __init__(self, book_id, book_name, auther, year_published, publisher):
        self.__book_id = book_id
        self.__book_name = book_name
        self.__auther = auther
        self.__year_published = year_published
        self.__publisher = publisher
        Book.counter += 1

    @property
    def book_id(self):
        return self.__book_id

    #add test for book_id length
    @book_id.setter
    def book_id(self, book_id):
        if type(book_id) == int:
            self.__book_id = book_id
        else:
            raise TypeError("Book ID must be an integer")

    @property
    def book_name(self):
        return self.__book_name

    @book_name.setter
    def book_name(self, book_name):
        if type(book_name) == str:
            self.__book_name = book_name
        else:
            raise TypeError("Book name must be a string")

    @property
    def auther(self):
        return self.__auther

    @auther.setter
    def auther(self, auther):
        if type(auther) == str:
            self.__auther = auther
        else:
            raise TypeError("Auther name must be a string")

    @property
    def year_published(self):
        return self.__year_published

    #fix date test
    @year_published.setter
    def year_published(self, year):
        if type(year) == str and len(year) == 4:
            self.__year_published = year
        else:
            raise TypeError("year must be a string such as YYYY")

    @property
    def publisher(self):
        return self.__publisher

    @publisher.setter
    def publisher(self, name):
        if type(name) == str:
            self.__publisher = name
        else:
            raise TypeError("Publisher name must be a string")


class Branch:
    counter = 0

    def __init__(self, name, phone, address):
        self.__name = name
        self.__phone = phone
        self.__address = address
        Branch.counter += 1

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address

