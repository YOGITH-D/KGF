from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mining.db'
app.config['SECRET_KEY']='6d7b2ce322ee4f25d933fccf'
bycrypt=Bcrypt(app)
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"
from mining import routes

