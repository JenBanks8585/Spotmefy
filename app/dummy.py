@appli.route('/recommend', methods=['POST'])
def recommend():

    df=pd.read_csv('https://raw.githubusercontent.com/Build-Week-Spotify-Song-Suggester-5/Data-Science/master/app/most_popular_spotify_songs.csv')
    df['song_id']= np.arange(0, len(df))

    if request.method == "POST":
        track_id = request.form['trackquery']

        print(track_id)

        song_id = df[df['track_id']== "1fe09crBtSIpU12St9WGPQ"].song_id.to_numpy()[0]

        print(song_id)

        _, neighbors = neigh.kneighbors(np.array([X_df.values[song_id]]))      
        five_neighs= list(neighbors[0])[1:]
        
        recs_song = []
        for item in five_neighs:
            row = df.iloc[item]
            recs_song.append((row.track_id, row.artist_name, row.track_name))  
            recs_song_df = pd.DataFrame(recs_song, columns =['track_id', 'artist_name','track_name'])
            recs_json = recs_song_df.to_json(orient = 'columns')
            parsed = json.loads(recs_json)  

        #return render_template('track_results.html', results = parsed)
        return parsed
