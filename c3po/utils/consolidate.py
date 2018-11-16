def __first(iterable, default=None):
    for item in iterable:
        return item
    return default


def artists(metadata):
    artists = []
    spotify_success = False
    try:
        spotify_artists = metadata['spotify']['tracks']['items'][0]['artists']
        for artist in spotify_artists:
            artists.append({
                "name": artist['name'],
                "spotify_id": artist['id'],
                "musixmatch_id": -1
            })
        spotify_success = True
    except IndexError:
        pass
    try:
        musixmatch_tracks = metadata['musixmatch']['message']['body'][
            'track_list']
        musixmatch_tracks = sorted(
            musixmatch_tracks,
            key=lambda x: x['track']['track_rating'],
            reverse=True)
        musixmatch_track = musixmatch_tracks[0]['track']
        match = __first(
            x for x in artists
            if x['name'].lower() == musixmatch_track['artist_name'].lower())
        if match:
            match['musixmatch_id'] = str(musixmatch_track['artist_id'])
        else:
            if spotify_success:
                # TODO: Add method to get MusixMatch Artist IDs using the ones Spotify has detected
                pass
            else:
                artists.append({
                    "name":
                    musixmatch_track['artist_name'],
                    "spotify_id":
                    -1,
                    "musixmatch_id":
                    str(musixmatch_track['artist_id'])
                })
    except IndexError:
        pass
    return artists


def song(metadata):
    song = None
    try:
        song_object = metadata['spotify']['tracks']['items'][0]
        song = {
            'name': song_object['name'],
            'spotify_id': song_object['id'],
            'musixmatch_id': -1
        }
    except IndexError:
        pass
    try:
        musixmatch_tracks = metadata['musixmatch']['message']['body'][
            'track_list']
        musixmatch_tracks = sorted(
            musixmatch_tracks,
            key=lambda x: x['track']['track_rating'],
            reverse=True)
        song_object = musixmatch_tracks[0]['track']
        if song:
            if song_object['track_name'].lower() == song['name'].lower():
                song['musixmatch_id'] = song_object['track_id']
        else:
            song = {
                'name': song_object['track_name'],
                'spotify_id': -1,
                'musixmatch_id': song_object['track_id']
            }
    except IndexError:
        pass
    return song


def genres(metadata):
    genres = {}
    try:
        musixmatch_tracks = metadata['musixmatch']['message']['body'][
            'track_list']
        musixmatch_tracks = sorted(
            musixmatch_tracks,
            key=lambda x: x['track']['track_rating'],
            reverse=True)
        song_object = musixmatch_tracks[0]['track']
        genres['primary'] = song_object['primary_genres']['music_genre_list']
        genres['secondary'] = song_object['secondary_genres'][
            'music_genre_list']
    except IndexError:
        pass
    return genres
