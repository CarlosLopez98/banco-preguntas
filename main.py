from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_preguntas.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development'
app.config['SECRET_KEY'] = "123456789"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
inspector = inspect(db.engine)

from views import *

login_manager.login_view = 'login'
login_manager.login_message = 'Es necesario iniciar sesión'
login_manager.login_message_category = 'warning'


if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
