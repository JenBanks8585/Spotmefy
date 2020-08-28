import pandas as pd
import numpy as np
import requests
import json
import pickle
import os

from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors
from sklearn.base import BaseEstimator, TransformerMixin

from flask import Blueprint, request, jsonify, render_template, Flask, redirect, url_for
#from flask_cors import CORS, cross_origin

model = Blueprint("model", __name__)


class My_encoder(BaseEstimator, TransformerMixin):
   
    def __init__(self,drop = 'first',sparse=False):
        self.encoder = OneHotEncoder(drop = drop,sparse = sparse)
        self.features_to_encode = []
        self.columns = []
    
    def fit(self,X_train,features_to_encode):
        
        data = X_train.copy()
        self.features_to_encode = features_to_encode
        data_to_encode = data[self.features_to_encode]
        self.columns = pd.get_dummies(data_to_encode,drop_first = True).columns
        self.encoder.fit(data_to_encode)
        return self.encoder
    
    def transform(self,X_test):
        
        data = X_test.copy()
        data.reset_index(drop = True,inplace =True)
        data_to_encode = data[self.features_to_encode]
        data_left = data.drop(self.features_to_encode,axis = 1)
        
        data_encoded = pd.DataFrame(self.encoder.transform(data_to_encode),columns = self.columns)
        
        return pd.concat([data_left,data_encoded],axis = 1)


df=pd.read_csv('https://raw.githubusercontent.com/Build-Week-Spotify-Song-Suggester-5/Data-Science/master/app/most_popular_spotify_songs.csv')
df['song_id']= np.arange(0, len(df))

features_to_encode = ['time_signature', 'mode', 'key', 'genre']             # features to encode
enc= My_encoder()                                                           # Instantiate encoder
enc.fit(df,features_to_encode)                                              # fit encoder
df_encoded = enc.transform(df)                                              # transform
features = df_encoded.columns.to_list()[4:]                                 # column names of numeric features
X = df_encoded[features].values                                             # numeric values
X_df = pd.DataFrame(X, columns = features )                                 # encoded df of selected features
  
neigh = NearestNeighbors(n_neighbors= 6)                                    # Instantiate NN
neigh.fit(X_df[features].values)                                            # fit 

# Pickling of files:

pickle.dump(neigh, open('neigh.pkl', 'wb'))

pickle.dump(X_df, open('X_df.pkl', 'wb'))

pickle.dump(df, open('df.pkl', 'wb'))

