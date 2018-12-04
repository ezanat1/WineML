import os
from flask import render_template,url_for,request,flash,redirect,jsonify
from wine import app
from wine import db
import requests
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,Length,ValidationError
from werkzeug.security import generate_password_hash,check_password_hash
from wine.models import User, Wine, UserChoice
from wine.wineClass import wineClassifier
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
import json

login_manager=LoginManager()
login_manager.init_app (app)
login_manager.login_view='login'


app_dir = os.path.realpath(os.path.dirname(__file__))
database_path = os.path.join(app_dir, "database.db")
print(database_path)
if not os.path.exists(database_path):
    print("building db")
    db.drop_all()
    db.create_all()
    print("end building db")

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

    #Validate if the username already exists in the database
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Thats username is already taken.Please choose another one')
    #Validate if the email already exists in the database
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken.Please choose another one')

class searchDashBoard(FlaskForm):
    wineName=StringField('wineName',validators=[DataRequired()])
    submit=SubmitField('Search')

@app.route('/',methods=['GET','POST'])
def index():
    form=wineForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user_input = form.name.data
        similar=a.getClosestMatch(user_input)[:9]
        if not similar:
            flash(' Wine Not found ')
        else:
            newList=[]
            for id in similar:
                print(id)
                info= a.getWineInfo(id)
                r=requests.get('https://www.vivino.com/api/wines/'+str(id)+'/wine_page_information').json()
                pic_url = r['wine_page_information']['vintage']['image']['location']
                info['url']="https:"+str(pic_url)
                newList.append(info)
                info=a.getWineInfo(id)
                if count > 8:
                    break
                if info['price']<=float(user_price):
                    r=requests.get('https://www.vivino.com/api/wines/'+str(id)+'/wine_page_information').json()
                    pic_url = r['wine_page_information']['vintage']['image']['location']
                    info['url']="https:"+str(pic_url)
                    newList.append(info)
                    count += 1
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
        return redirect (url_for('login'))
    return render_template('account.html',form=form)


@app.route('/dash',methods=['GET','POST'])
@login_required
def dashboard():
    # form=searchDashBoard(request.form)
    return render_template('dashboard.html',name=current_user.username)

@app.route('/save',methods=['GET','POST'])
@login_required
def save():
    user_id=current_user.get_id()
    print('the user id is ',user_id)
    wine_id=request.form['id']
    print(wine_id)
    preference=UserChoice(user_id=user_id,wine_id=wine_id)
    db.session.add(preference)
    db.session.commit()

    return jsonify({'result':'success'})

@app.route('/myWine')
@login_required
def myWine():
    # wines=UserChoice.query.all()
    return render_template('myWines.html')



@app.route('/process',methods=['POST'])
@login_required
def process():
    if current_user.is_authenticated:
            user_input=request.form['wineName']
            print(user_input)
            if user_input:
                similar=a.getClosestMatch(user_input)[:9]
                if not similar:
                    flash(' Wine Not found ')
                else:
                    newList=[]
                    for id in similar:
                        print(id)
                        info= a.getWineInfo(id)
                        r=requests.get('https://www.vivino.com/api/wines/'+str(id)+'/wine_page_information').json()
                        pic_url = r['wine_page_information']['vintage']['image']['location']
                        info['url']="https:"+str(pic_url)
                        newList.append(info)
                    return jsonify(newList)
            return jsonify({'error':'missing Data'})


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))