# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:45:34 2021

@author: Sanjay G R
"""

from flask import Flask, render_template,url_for,request
import pandas as pd
import pickle
from tensorflow import keras


app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)