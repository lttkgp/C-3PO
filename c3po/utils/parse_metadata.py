def parse_musixmatch(mm_data):
    try:
        song_title = mm_data['message']['body']['track_list'][0]['track'][
            'track_name']
    except Exception:
        song_title = None
    try:
        genre_name = mm_data['message']['body']['track_list'][0]['track'][
            'primary_genres']['music_genre_list'][0]['music_genre'][
                'music_genre_name']
    except Exception:
        genre_name = None
    try:
        artist_name = mm_data['message']['body']['track_list'][0]['track'][
            'artist_name']
    except Exception:
        artist_name = None
    return song_title, genre_name, artist_name


def parse_spotify(sp_data):
    try:
        song_title = sp_data['tracks']['items'][0]['name']
    except Exception:
        song_title = None
    try:
        artist_name = sp_data['tracks']['items'][0]['artists'][0]['name']
    except Exception:
        artist_name = None
    return song_title, artist_name
