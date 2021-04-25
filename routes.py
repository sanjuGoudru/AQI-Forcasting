# -*- coding: utf-8 -*-

from __main__ import app, models_test_rmse
from flask import render_template,redirect,url_for,session,Response,jsonify
from forms import AQIPredictionForm,LSTMForecastForm
from utils import Utils
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io,os

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


@app.route('/forecast', methods=['POST','GET'])
def lstm_forecast():
    form = LSTMForecastForm()
        
    if form.validate_on_submit():
        time_step = form.time_step.data
        data_size = form.data_size.data
        fig = Utils.get_lstm_forecast(time_step=time_step,data_size = data_size)
        
        if os.path.exists('static/temp_plots/plot.png'):
            os.remove("static/temp_plots/plot.png")
        
        fig.savefig('static/temp_plots/plot.png')
        return redirect(url_for('display_forecast'))
    return render_template('lstm_forecast.html',form=form)

@app.route('/display_forecast')
def display_forecast():
    return render_template('display_forecast.html')

@app.after_request
def add_header(response):
    
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response