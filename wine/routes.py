from flask import render_template
from wine import app

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from wine.models import wine

class wineForm(FlaskForm):
    name=StringField('Wine Name',validators=[DataRequired()])
    submit=SubmitField()

@app.route('/',methods=['GET','POST'])
def index():
    form=wineForm()
    if form.validate_on_submit():
        wines=wine.query.all()
        return render_template('rec.html',wines=wines)
    return render_template('index.html',form=form)