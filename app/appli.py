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

appli = Blueprint("appli", __name__)

neigh = pickle.load(open('neigh.pkl', 'rb'))
X_df = pickle.load(open('X_df.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))


def get_rec(track, return_json = True):
    
    song_id = df[df['track_id']== track].song_id.to_numpy()[0]

    _, neighbors = neigh.kneighbors(np.array([X_df.values[song_id]]))      
    five_neighs= list(neighbors[0])[1:]
        
    recs_song = []
    for item in five_neighs:
        row = df.iloc[item]
        recs_song.append((row.track_id, row.artist_name, row.track_name))  
        recs_song_df = pd.DataFrame(recs_song, columns =['track_id', 'artist_name','track_name'])
        recs_json = recs_song_df.to_json(orient = 'records')
            
    return recs_json


@appli.route('/<track>' , methods = ['GET'])
def trackid(track):
    return get_rec(track)


@appli.route('/')
def start():
    return render_template("track_id.html")


@appli.route('/recommend', methods=['POST'])
def recommend():

    if request.method == "POST":
        track_id = request.form['trackquery']

        song_id = df[df['track_id']== track_id].song_id.to_numpy()[0]

        _, neighbors = neigh.kneighbors(np.array([X_df.values[song_id]]))      
        five_neighs= list(neighbors[0])[1:]

        recs_song = []
        for item in five_neighs:
            row = df.iloc[item]
            recs_song.append((row.track_id, row.artist_name, row.track_name))  
            recs_song_df = pd.DataFrame(recs_song, columns =['track_id', 'artist_name','track_name'])
            recs_json = recs_song_df.to_json(orient = 'columns')
        

        return recs_json





