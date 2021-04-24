# -*- coding: utf-8 -*-


import pickle
import numpy as np
#model = keras.models.load_model('./Data/Models/lstm2_regression.h5')


def get_season(month):
    season_dict = pickle.load(open('Data/season_map.pkl','rb'))
    return season_dict[month]


def process_form_data(form):
    data = dict()
    data['PM2_5'] = form.pm2_5.data
    data['PM10'] = form.pm10.data
    data['NO'] = form.no.data
    data['NO2'] = form.no2.data
    data['NOx'] = form.nox.data
    data['NH3'] = form.nh3.data
    data['CO'] = form.co.data
    data['SO2'] = form.so2.data
    data['O3'] = form.o3.data
    data['Benzene'] = form.benzene.data
    data['Toluene'] = form.toluene.data
    datetime = form.toluene.data
    month = datetime.month
    time = f"{datetime.hour}:00:00"
    season = get_season(month)
    data['Time_Season_Mean'] = time + season
    return data


def scale_data(data):
    time_season_map = pickle.load(open('Data/time_season_dict.pkl','rb'))
    data['Time_Season_Mean'] = time_season_map[data['Time_Season_Mean']]
    
    sc_X = pickle.load(open('Data/X_scaler.pkl', 'rb'))
    X = []
    for key,value in data.items():
        X.append(value)
    X_scaled = sc_X.transform(X)
    return X_scaled

def scale_aqi(y):
    sc_y = pickle.load(open('Data/y_scaler.pkl', 'rb'))
    y_scaled = sc_y.inverse_transform(np.array(y).reshape(-1,1))
    return y_scaled
    

def predict(data,model_name=None):
    scaled_data = scale_data(data)
    
    models = dict()
    if model_name == 'XGB':
        models['XGB'] = pickle.load(open('Data/Models/xgb_regression.pkl','rb'))

    aqi = dict()    
    for mod_name, model in models.items():
        temp = model.predict(scaled_data)
        aqi[mod_name] = scale_aqi(aqi[mod_name])
    
    return aqi


    