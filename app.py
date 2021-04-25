# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:45:34 2021

@author: Sanjay G R
"""

from flask import Flask
import pickle
from tensorflow import keras


def load_models():
    models = dict()
    models['lr'] = pickle.load(open('Data/Models/linear_regression.pkl','rb'))
    models['ridge'] = pickle.load(open('Data/Models/ridge_regression.pkl','rb'))
    models['lasso'] = pickle.load(open('Data/Models/lasso_regression.pkl','rb'))
    models['dtree'] = pickle.load(open('Data/Models/dtree_regression.pkl','rb'))
    models['svm'] = pickle.load(open('Data/Models/svm_regression.pkl','rb'))
    models['xgb'] = pickle.load(open('Data/Models/xgb_regression.pkl','rb'))
    models['lstm'] = keras.models.load_model('Data/Models/lstm2_regression.h5')
    return models
    

def get_test_rmse():
    rmse_dict = dict()
    rmse_dict['lr'] = 24.39
    rmse_dict['ridge'] = 21.12
    rmse_dict['lasso'] = 25.72
    rmse_dict['dtree'] = 23.76
    rmse_dict['xgb'] = 20.09
    rmse_dict['svm'] = 24.34
    return rmse_dict
    
    
models = load_models()
models_test_rmse = get_test_rmse()    



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
import routes

if __name__ == '__main__':
    app.run(debug=True)
    

