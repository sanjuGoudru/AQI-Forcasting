# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:45:34 2021

@author: Sanjay G R
"""

import os
from flask import Flask,render_template,redirect,url_for,session
import pickle
from tensorflow import keras
from forms import AQIPredictionForm,LSTMForecastForm
import pandas as pd, numpy as np
from utils import Utils


def load_models():
    models = dict()
    models['lr'] = pickle.load(open('Data/Models/linear_regression.pkl','rb'))
    models['ridge'] = pickle.load(open('Data/Models/ridge_regression.pkl','rb'))
    models['lasso'] = pickle.load(open('Data/Models/lasso_regression.pkl','rb'))
    models['dtree'] = pickle.load(open('Data/Models/dtree_regression.pkl','rb'))
    models['svm'] = pickle.load(open('Data/Models/svm_regression.pkl','rb'))
    #models['xgb'] = pickle.load(open('Data/Models/xgb_regression.pkl','rb'))
    models['lstm'] = keras.models.load_model('Data/Models/lstm2_regression.h5')
    return models
    

def get_test_rmse():
    rmse_dict = dict()
    rmse_dict['lr'] = 24.39
    rmse_dict['ridge'] = 21.12
    rmse_dict['lasso'] = 25.72
    rmse_dict['dtree'] = 23.76
    #rmse_dict['xgb'] = 20.09
    rmse_dict['svm'] = 24.34
    return rmse_dict
    
def predict_res(data,model_name=None):
    scaled_data = Utils.scale_data(data)
    df = pd.DataFrame(scaled_data,columns=['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Time_Season_Mean'])
        
    aqi = dict()

    for mod_name, model in models.items():
        if mod_name=='lstm':
            continue
        temp = model.predict(df)
        aqi[mod_name] = Utils.scale_aqi(temp)
        
    return aqi
    
    
def get_lstm_forecast(time_step,data_size):
    print("\n\n---------------------\n\n")
    print(f"time_step:{time_step}\n data_size:{data_size}\n")
    print("\n\n---------------------\n\n")
            
    X,y = Utils.load_test_data()
    data = pd.concat([X,y],axis=1)
            
    n_steps = 40
    X,y = Utils.split_sequences(data.to_numpy(),n_steps=n_steps)
            
    print("\n\n---------------------\n\n")
    print(f"X:{X.shape}\n y:{y.shape}\n")
    print("\n\n---------------------\n\n")
            
    model = models['lstm']
    sc_y = pickle.load(open('Data/y_scaler.pkl', 'rb'))
            
    X_input = X[-(data_size+time_step):]
    y_input = y[-(data_size+time_step):]
            
    print("\n\n---------------------\n\n")
    print(f"X_input:{X_input.shape}\ny_input:{y_input.shape}\n")
    print("\n\n---------------------\n\n")
            
    true_aqi, pred_aqi = Utils.get_forecast(X_input, y_input, time_step, data_size,model)
                
    before_aqi = sc_y.inverse_transform(y[-(data_size+30):-data_size,-1].reshape(-1, 1))
    true_aqi = sc_y.inverse_transform(np.array(true_aqi).reshape(-1, 1))
    pred_aqi = sc_y.inverse_transform(np.array(pred_aqi).reshape(-1, 1))
            
    img = Utils.get_image(before_aqi,true_aqi,pred_aqi,data_size)
            
    return img


models = load_models()
models_test_rmse = get_test_rmse()    

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

from utils import Utils


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
    aqi = predict_res(data)
    return render_template('result.html',aqi_dict=aqi,models_test_rmse=models_test_rmse)


@app.route('/forecast', methods=['POST','GET'])
def lstm_forecast():
    form = LSTMForecastForm()
        
    if form.validate_on_submit():
        time_step = form.time_step.data
        data_size = form.data_size.data
        fig = get_lstm_forecast(time_step=time_step,data_size = data_size)
        
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

if __name__ == '__main__':
    app.run(debug=True)
    

