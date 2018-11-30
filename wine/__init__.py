from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_material import Material


app=Flask(__name__,static_folder='static')
app.config['SECRET_KEY']='strongPassword123'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
Material(app)
db=SQLAlchemy(app)

from wine import routes
