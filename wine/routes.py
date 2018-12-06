import os
from flask import render_template,url_for,request,flash,redirect,jsonify,session
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
    name=StringField('Enter a Vineyard or Varietal',validators=[DataRequired()])
    price=StringField('Enter the Max Price of Output Wines',validators=[DataRequired()])
    food=StringField('Choose Food Pairing From: Game, Fish, Vegetarian, '+ 
    'Pasta, Poultry, Pork, Spicy, Seafood, Shellfish, Veal, Cheese, '+
    'Lamb, Mushrooms, Beef, Cured Meat, Desserts',validators=[DataRequired()])
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
        user_price = form.price.data
        user_food=form.food.data
        wineID=a.getIdByName(user_input)
        similar=a.getClosestMatch(wineID,[user_food])
        if not similar:
            flash(' Wine Not found ')
        else:
            newList=[]
            count = 0
            for id in similar:
                info=a.getWineInfo(id)
                if count > 8:
                    break
                if info['price']<=float(user_price):
                    r=requests.get('https://www.vivino.com/api/wines/'+str(id)+'/wine_page_information').json()
                    pic_url = r['wine_page_information']['vintage']['image']['location']
                    info['url']="https:"+str(pic_url)
                    info['pairing']= getPairings(info['variance'])
                    newList.append(info)
                    count += 1
            return render_template('rec.html',newList=newList,user_input=user_input)

    return render_template('index.html',form=form)

def getPairings(varietal):
    ref = ['Game', 'Fish', 'Vegetarian', 
    'Pasta', 'Poultry', 'Pork', 'Spicy', 'Seafood', 
    ' Poultry', ' Shellfish', 'Veal', 'Cheese', 
    'Lamb', 'Mushrooms', 'Beef', 'Cured Meat', 
    'Shellfish', 'Desserts']

    wines = {'Agiorgitiko': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0], 
    'Albariño': [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
    'Aragonez': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0], 
    'Arinto de Bucelas': [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
    'Arneis': [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0], 
    'Baga': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Barbera': [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
    'Blaufränkisch': [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
    'Cabernet Franc': [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0], 
    'Cabernet Sauvignon': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Carménère': [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Chardonnay': [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    'Chenin Blanc': [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
    'Cortese': [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Corvina': [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0], 
    'Gamay': [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
    'Gewürztraminer': [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
    'Glera (Prosecco)': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
    'Grüner Veltliner': [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
    'Grenache': [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Grenache Blanc': [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
    'Malagouzia': [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
    'Malbec': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Malvasia': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Melon de Bourgogne': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    'Mencia': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
    'Merlot': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0], 
    'Montepulciano': [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
    'Moscatel de Alejandría': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    'Moscatel de grano menudo': [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
    'Moscato': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    'Mourvedre': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Nebbiolo': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Palomino': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], 
    'Petite Sirah': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Pinot Blanc': [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0], 
    'Pinot Grigio': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], 
    'Pinot Gris': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], 
    'Pinot Noir': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
    'Pinotage': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
    'Primitivo': [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Riesling': [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
    'Roussanne': [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
    'Sangiovese': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0], 
    'Sauvignon Blanc': [1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
    'Savagnin': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0], 
    'Shiraz/Syrah': [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0], 
    'Silvaner': [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
    'Tannat': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Tempranillo': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0], 
    'Torrontés': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    'Touriga Nacional': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0], 
    'Trebbiano': [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
    'Verdejo': [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
    'Verdelho': [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
    'Viognier': [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
    'Viura': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
    'Xarel-lo': [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    'Xinomavro': [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
    'Zinfandel': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0]}

    vector = wines[varietal]
    food_list = []
    for index in range(len(vector)):
        if vector[index] == 1:
            food_list.append(ref[index])
    food_list = ", ".join(food_list)
    return food_list

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
    return render_template('dashboard.html',name=current_user.username)

@app.route('/process',methods=['POST'])
@login_required
def process():
    if current_user.is_authenticated:
            user_input=request.form['wineName']
            user_price = request.form['price']
            user_price=float(user_price)
            # user_food = request.form['userFood']
            wineID=a.getIdByName(user_input)
            similar=a.getClosestMatch(wineID)
            if not similar:
                flash(' Wine Not found ')
            else:
                newList=[]
                count = 0
                for id in similar:
                    info=a.getWineInfo(id)
                    if count > 8:
                        break
                    if info['price']<=float(user_price):
                        r=requests.get('https://www.vivino.com/api/wines/'+str(id)+'/wine_page_information').json()
                        pic_url = r['wine_page_information']['vintage']['image']['location']
                        info['url']="https:"+str(pic_url)
                        info['pairing']= getPairings(info['variance'])
                        newList.append(info)
                        count += 1

                return jsonify(newList)
            return jsonify({'error':'missing Data'})

@app.route('/save',methods=['GET','POST'])
@login_required
def save():
    user_id=current_user.get_id()
    wine_id=request.form['id']
    preference=UserChoice(user_id=user_id,wine_id=wine_id)
    db.session.add(preference)
    db.session.commit()
    flash('Your Wine is Saved')
    return jsonify({'result':'success'})

@app.route('/myWine')
@login_required
def myWine():
    user_id1=current_user.get_id()
    wines=UserChoice.query.filter_by(user_id=user_id1)
    wineID=[w.wine_id for w in wines]
    newList=[]
    for w in wineID:
        info=a.getWineInfo(w)
        r=requests.get('https://www.vivino.com/api/wines/'+str(w)+'/wine_page_information').json()
        pic_url = r['wine_page_information']['vintage']['image']['location']
        info['url']="https:"+str(pic_url)
        info['pairing']= getPairings(info['variance'])
        newList.append(info)
    return render_template('myWines.html',newList=newList)

@app.route('/deleteWine', methods=['POST'])
@login_required
def deleteWine():
        user_id=current_user.get_id()
        wine_id=request.form['id']
        # wine=UserChoice(user_id=user_id,wine_id=wine_id)
        wine=UserChoice.query.filter_by(wine_id=wine_id).first()
        db.session.delete(wine)
        db.session.commit()
        return jsonify({'result':wine_id})
        return redirect(url_for('myWine'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))