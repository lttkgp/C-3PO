import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fetch_songs import get_song_url
from music_metadata_extractor import SongData

scope="playlist-modify-public"
username=os.getenv("SPOTIFY_USERNAME")
token = SpotifyOAuth(scope=scope,username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

 # fetch spotify uri
list_of_songs = get_song_url()

# fetch latest created playlist id
playlist_id = os.getenv("SPOTIFY_PLAYLIST_ID")

# add songs to playlist
spotifyObject.user_playlist_replace_tracks(user=username,playlist_id=playlist_id,tracks=list_of_songs)