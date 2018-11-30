from wine import db
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(80))