from flask import Flask
from flaskext.mysql import MySQL
from flask_session import Session


app = Flask(__name__)
mysql = MySQL()
app.config['SECRET_KEY'] = '5479437c16e750c4c8e3a432fe891395'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Shlomo1995'
app.config['MYSQL_DATABASE_DB'] = 'ProjectLibraries'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor()
from ProjectApp import routes


