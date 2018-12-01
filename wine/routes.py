from flask import render_template,url_for,request,flash,redirect
from wine import app
from wine import db
import requests
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,Length
from werkzeug.security import generate_password_hash,check_password_hash
from wine.models import User
from wine.wineClass import wineClassifier
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
import json

login_manager=LoginManager()
login_manager.init_app (app)
login_manager.login_view='login'
a = wineClassifier()

class wineForm(FlaskForm):
    name=StringField('Wine Name',validators=[DataRequired()])
    submit=SubmitField()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class loginForm(FlaskForm):
    username=StringField('User name',validators=[DataRequired(),Length(min=5,max=15)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=5,max=15)])
    remember=BooleanField()
    submit=SubmitField('Log in')

class registerForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email(message='Invalid Email'),Length(max=50)])
    username=StringField('User name',validators=[DataRequired(),Length(min=5,max=15)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=5,max=15)])
    submit=SubmitField('Sign up')

@app.route('/',methods=['GET','POST'])
def index():
    form=wineForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user_input = form.name.data
        wineInfo=a.getWineInfo(user_input)
        similar=a.getClosestMatch(user_input)[:9]
        if not similar:
            flash(' Wine Not found ')
        else:
            newList=[]
            for id in similar:
                info=a.getWineInfo(id)
                r=requests.get('https://www.vivino.com/api/wines/'+str(id)+'/wine_page_information').json()
                pic_url = r['wine_page_information']['vintage']['image']['location']
                info['url']="https:"+str(pic_url)
                newList.append(info)
            return render_template('rec.html',newList=newList,user_input=user_input)
    return render_template('index.html',form=form)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/login',methods=['GET','POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1> invalid password'
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form=registerForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data,method='sha256')
        new_user =User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return "<h1> Succesfully Registered"
    return render_template('account.html',form=form)

@app.route('/dash')
@login_required
def dashboard():
    return render_template('dashboard.html',name=current_user.username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))