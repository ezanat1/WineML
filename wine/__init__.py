from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_material import Material  

app=Flask(__name__)
app.config['SECRET_KEY']='strongPassword123'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
Material(app)
db=SQLAlchemy(app)

from wine import routes
