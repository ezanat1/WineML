# Project-Team-9
Student Names: Steven Duong,​ ​Ezana Tesfaye, Lishan Zhu, Shengqi Suizhu
Team Name: Pioneers
 
Project title: Wine Recommender  - APPROVED
 
Project description: Sometimes when people find a type of wine they enjoy, they are likely to try similar types of wine.
With this project, the user will be able to input a group of wines he/she like, and set filters for attributes such as price, region, or varietal. The model then recommends new wines to the user that it thinks he/she would like. Similarity will be calculated based on attributes such as varietal, region, previous user’s reviews, and keywords from the wine’s description.
 
Proposed methodology/ resources, etc: We’ll be using sentiment analysis to determine the similarity between each wine’s description and factor that into the overall similarity of each wine. Then a classifier is used to match the description of the user input and then return the types of wine that matches the input.
 
Data set: fetched from https://www.vivino.com/

## Website

[Wine Recommendation Site](http://3.16.160.236)


## Install dependencies

pip install flask

pip install Flask-Materialize

pip install flask_wtf

pip install flask_sqlalchemy

pip install flask_login

pip install Pillow

pip install bcrypt

pip install fuzzywuzzy

pip install numpy

pip install pickle

## Run code

cd to main directory where run.py is

python run.py

## Screenshots:
![Home page](https://github.com/SJSU272LabF18/Project-Team-9/blob/master/demo/1.png)
![Wine list](https://github.com/SJSU272LabF18/Project-Team-9/blob/master/demo/2.png)
![Log in](https://github.com/SJSU272LabF18/Project-Team-9/blob/master/demo/3.png)
![Register](https://github.com/SJSU272LabF18/Project-Team-9/blob/master/demo/4.png)
![Dashboard](https://github.com/SJSU272LabF18/Project-Team-9/blob/master/demo/5.png)
![Selection](https://github.com/SJSU272LabF18/Project-Team-9/blob/master/demo/6.png)
