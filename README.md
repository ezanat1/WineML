# Project-Team-9
Student Names: Steven Duong,​ ​Ezana Tesfaye, Lishan Zhu, Shengqi Suizhu
Team Name: Pioneers
 
Project title: Wine Recommender  - APPROVED
 
Project description: Sometimes when people find a type of wine they enjoy, they are likely to try similar types of wine.
With this project, the user will be able to input a group of wines he/she like, and set filters for attributes such as price, region, or varietal. The model then recommends new wines to the user that it thinks he/she would like. Similarity will be calculated based on attributes such as varietal, region, previous user’s reviews, and keywords from the wine’s description.
 
Proposed methodology/ resources, etc: We’ll be using sentiment analysis to determine the similarity between each wine’s description and factor that into the overall similarity of each wine. Then a classifier is used to match the description of the user input and then return the types of wine that matches the input.
 
Data set: fetched from https://www.vivino.com/



# Run code

Create virtual environment 

python3 -m venv venv

After init virtual environment --> activate virtual environment

source venv/bin/activate

python3 run.py


## Install dependencies

pip3 install flask

pip3 install Flask-Materialize

pip3 install flask_wtf

pip3 install flask_sqlalchemy


## Install dependencies in wine blog
pip install flask

pip install flask_sqlalchemy

pip install flask_wtf

pip install bcrypt

pip install flask_login

pip install Pillow

 
 


