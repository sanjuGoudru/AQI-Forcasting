# -*- coding: utf-8 -*-

from __main__ import app
from flask import render_template,redirect,url_for,session
from forms import AQIPredictionForm
from utils import Utils,models_test_rmse

@app.route('/', methods=['POST','GET'])
def home():
    form = AQIPredictionForm()
        
    if form.validate_on_submit():
        data = Utils.process_form_data(form)
        session['data']=data
        return redirect(url_for('predict'))
    return render_template('home.html',form=form)



@app.route('/predict')
def predict():
    data = session['data']
    aqi = Utils.predict_res(data)
    return render_template('result.html',aqi_dict=aqi,models_test_rmse=models_test_rmse)


@app.route('/forecast')
def lstm_forecast():
    return render_template('lstm_forecast.html')