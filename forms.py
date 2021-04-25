# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField,FloatField,DateTimeField
from wtforms.validators import DataRequired,NumberRange
class AQIPredictionForm(FlaskForm):
    pm2_5 = FloatField('PM 2.5',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    pm10 = FloatField('PM 10',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    no = FloatField('NO',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    no2 = FloatField('NO2',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    nox = FloatField('NOx',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    nh3 = FloatField('NH3',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    co = FloatField('CO',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    so2 = FloatField('SO2',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    o3 = FloatField('O3',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    benzene = FloatField('Benzene',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    toluene = FloatField('Toluene',
                       validators=[DataRequired('This field cannot be empty'),
                                   NumberRange(min=0.0,message="This field should be positive")])
    date_time = DateTimeField('Date and Time',id='datetime')
    
    submit = SubmitField("Predict AQI")
    