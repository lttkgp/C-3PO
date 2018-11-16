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
            x for x in artists if x['name'] == musixmatch_track['artist_name'])
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
