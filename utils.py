# -*- coding: utf-8 -*-


import pickle
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

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
    def load_test_data():
        X = pd.read_csv('Data/Final/X_test_sc.csv')
        y = pd.read_csv('Data/Final/y_test_sc.csv')
        return X,y
    
    @staticmethod
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the dataset
            if end_ix > len(sequences)-1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y)
    
    @staticmethod
    def get_forecast(X_input, y_input, time_step, data_size,model):
        pred_aqi = []
        true_aqi = []
        if time_step == 0:
            y_pred = model.predict(X_input)
            true_aqi = y_input[:,-1]
            pred_aqi = y_pred[:,-1]
            return true_aqi, pred_aqi 
        i=0
        while i<data_size:
            temp_inp = X_input[i]

            pred = model.predict(temp_inp.reshape(1,temp_inp.shape[0],temp_inp.shape[1]))
    
            for j in range(time_step):
                temp_inp = np.concatenate((temp_inp, pred),axis=0)
                temp_inp = temp_inp[1:]
                pred = model.predict(temp_inp.reshape(1,temp_inp.shape[0],temp_inp.shape[1]))
            
            pred_aqi.append(pred[0,-1])
            true_aqi.append(y_input[i+time_step,-1])
        
            i = i+1
        return true_aqi, pred_aqi
        
    
    
    @staticmethod
    def get_image(before_aqi,true_aqi,pred_aqi,data_size):
        fig = Figure(figsize=(10,4))
        axis = fig.add_subplot(1, 1, 1)
        print("\n\n---------------------\n\n")
        print(f"before_aqi:{before_aqi.shape}\ntrue_aqi:{true_aqi.shape}\npred_aqi:{pred_aqi.shape}")
        print(len(range(len(before_aqi),(data_size+len(before_aqi)))))
        print("\n\n---------------------\n\n")
        axis.plot(range(0,len(before_aqi)),before_aqi,'b',label='Before Data')
        axis.plot(range(len(before_aqi),(data_size+len(before_aqi))), true_aqi,'b--',label='Real Data')
        axis.plot(range(len(before_aqi),(data_size+len(before_aqi))),pred_aqi,'r',label='Predicted Data')
        axis.legend()
        return fig