from flask import Flask
from flaskext.mysql import MySQL
from flask_session import Session


app = Flask(__name__)
mysql = MySQL()
app.config['SECRET_KEY'] = '5479437c16e750c4c8e3a432fe891395'
app.config['MYSQL_DATABASE_HOST'] = '34.165.221.110'
app.config['MYSQL_DATABASE_USER'] = 'group28'
app.config['MYSQL_DATABASE_PASSWORD'] = '6jyaw40q'
app.config['MYSQL_DATABASE_DB'] = 'group28_db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor()
from ProjectApp import routes


