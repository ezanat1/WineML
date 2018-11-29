from flask import render_template,url_for,request,flash
from wine import app
import requests

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired
from wine.models import wine
from wine.wineClass import wineClassifier



a = wineClassifier()

class wineForm(FlaskForm):
    name=StringField('Wine Name',validators=[DataRequired()])
    submit=SubmitField()
    
class loginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Log in')

class registerForm(FlaskForm):
    firstName=StringField('First Name',validators=[DataRequired()])
    lastName=StringField('Last Name',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirmPassword=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField('Sign up')

@app.route('/',methods=['GET','POST'])
def index():
    form=wineForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # wines=wine.query.all()
        user_input = form.name.data
        wineInfo=a.getWineInfo(user_input)
        # similar=a.getWineInfo(a.getClosestMatch(user_input)[0])
        # print(similar[:10])
        similar=a.getClosestMatch(user_input)[:10]
        API_KEY='e34875d11fcaa37dc08ce32849965d22ecde47852672a7f8706b43a7086485ac'
        r=requests.get('https://api.unsplash.com/photos/?client_id='+ API_KEY)
        if not similar:
            flash(' Wine Not found ')
        else:
            newList=[]
            for id in similar:
                info=a.getWineInfo(id)
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
        return render_template('rec.html')
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form=registerForm()
    if form.validate_on_submit():
        return render_template('rec.html')
    return render_template('account.html',form=form)

@app.route('/account',methods=['GET','POST'])
def account():
    return render_template('myWine.html')
# Wine A: {'rating': 3.7, 'price': 18.76, 'sentiment': 0.6183475748225075, 'variance': 'Cabernet Sauvignon', 'vineyard': 'Château de la Dauphine', 'region': 'Fronsac'}
# Wine that is similar: {'rating': 3.7, 'price': 17.99, 'sentiment': 0.5325739483137195, 'variance': 'Cabernet Sauvignon', 'vineyard': 'Château Mayne-Vieil', 'region': 'Fronsac'}