from wine import db
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(80))


class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    rating = db.Column(db.Float)
    price = db.Column(db.Float)
    sentiment = db.Column(db.Float)
    variance = db.Column(db.String(255))
    vineyard = db.Column(db.String(255))
    region = db.Column(db.String(255))
