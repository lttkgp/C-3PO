import os
import re
from dotenv import load_dotenv, find_dotenv
from music_metadata_extractor import SongData
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# env variables: SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIFY_USERNAME, PLAYLIST_ID
load_dotenv(find_dotenv())
USERNAME = os.getenv('SPOTIPY_USERNAME')
PLAYLIST_ID = os,getenv('PLAYLIST_ID')
SCOPE='playlist-modify-public'


def _get_spotify_client():
    return Spotify(auth_manager=SpotifyOAuth(username=USERNAME, scope=SCOPE))

def add_song_to_playlist(spotify_track_id):
    spotify_client = _get_spotify_client()
    user_id = spotify_client.current_user()['id']
    spotify_client.user_playlist_add_tracks(user=user_id, playlist_id=PLAYLIST_ID, tracks=[spotify_track_id])

def get_spotify_id(url):
    spotify_pattern = re.compile(
        r"""
        https?:\/\/open\.spotify\.com\/track\/(?P<id>[a-zA-Z0-9]+)
        """,
        re.VERBOSE
    )
    spotify_match = spotify_pattern.match(url)
    if spotify_match:
        return spotify_match.group("id")
    else:
        yt_pattern = re.compile(
            r"""
            (https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.
            (com|be)/(watch\?v=|embed/|v/|.+\?v=)?
            (?P<id>[A-Za-z0-9\-=_]{11})""",
            re.VERBOSE,
        )
        yt_match = yt_pattern.match(url)
        if(yt_match):
            data = SongData(url)
            if data.track:
                return data.track.provider_id



