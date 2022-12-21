from __init__ import app
from flask import render_template

@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/register_librarian')
def register_librarian():
    return render_template('register_librarian.html')

@app.route('/register_user')
def register_user():
    return render_template('register_user.html')

@app.route('/homepage_librarian')
def homepage_librarian():
    return render_template('homepage_librarian.html')

@app.route('/homepage_user')
def homepage_user():
    return render_template('homepage_user.html')

@app.route('/login')
def login():
    return render_template('login.html')