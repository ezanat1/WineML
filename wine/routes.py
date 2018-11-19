from flask import render_template,url_for
from wine import app

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired
from wine.models import wine

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
    form=wineForm()
    if form.validate_on_submit():
        wines=wine.query.all()
        return render_template('rec.html',wines=wines)
    return render_template('index.html',form=form)

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