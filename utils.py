# -*- coding: utf-8 -*-


import pickle
import numpy as np
import pandas as pd
from __main__ import models,models_test_rmse
class Utils:
    
    @staticmethod
    def get_season(month):
        season_dict = pickle.load(open('Data/season_map.pkl','rb'))
        return season_dict[month]
    
    @staticmethod
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
        month = form.date_time.data.month
        hour = form.date_time.data.strftime('%H')
        time = f"{hour}:00:00"
        season = Utils.get_season(month)
        data['Time_Season_Mean'] = time + season
        return data
    
    @staticmethod
    def scale_data(data):
        time_season_map = pickle.load(open('Data/time_season_dict.pkl','rb'))
        data['Time_Season_Mean'] = time_season_map[data['Time_Season_Mean']]
        
        sc_X = pickle.load(open('Data/X_scaler.pkl', 'rb'))
        X = []
        for key,value in data.items():
            X.append(value)
        X_scaled = sc_X.transform(np.array(X).reshape(1,-1))
        return X_scaled
    
    @staticmethod
    def scale_aqi(y):
        sc_y = pickle.load(open('Data/y_scaler.pkl', 'rb'))
        y_scaled = sc_y.inverse_transform(np.array(y).reshape(-1,1))
        return y_scaled
        
    @staticmethod
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
    
    