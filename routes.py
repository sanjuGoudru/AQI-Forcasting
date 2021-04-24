# -*- coding: utf-8 -*-

from app import app
from flask import render_template,redirect,url_for,request
from forms import AQIPredictionForm
from utils import predict,process_form_data

@app.route('/', methods=['POST'])
def home():
    form = AQIPredictionForm()
    
    if form.validate_on_submit():
        data = process_form_data(form)
        return redirect(url_for('predict',data=data))
    return render_template('home.html',form=form)

@app.route('/predict')
def predict():
    data = request.args['data']
    aqi = predict(data,model_name='XGB')
    return render_template('predict.html',aqi=aqi)