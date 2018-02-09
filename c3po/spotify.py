"""
Spotify setup
"""
import os
from os.path import abspath, dirname, join
import spotipy
import spotipy.util as spotipy_util
from dotenv import load_dotenv

DOTENV_PATH = join(dirname(dirname(abspath(__file__))), '.env')
load_dotenv(DOTENV_PATH)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost/"
SPOTIFY_TOKEN = spotipy_util.prompt_for_user_token(
    '22gndvram3iydupmjvgg7fz2a', 'user-read-email', SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI)
SPOTIFY = spotipy.Spotify(auth=SPOTIFY_TOKEN)

def search_sp(query):
    """
    Method to search for a track using Spotify API
    """
    response = SPOTIFY.search(q=query, type='track')
    return response
