"""
Core script. Structure to be changed later.
"""
import os
from os.path import join
import re
import warnings
import dotenv
from dotenv import find_dotenv, load_dotenv
import requests
import spotipy
import spotipy.util as spotipy_util

from helpers import SEPARATORS

DOTENV_PATH = join(os.path.pardir, '.env')
load_dotenv(DOTENV_PATH)

REQ_SESSION = requests.Session()
FB_URL = 'https://graph.facebook.com/v2.11/'
FB_SHORT_ACCESS_TOKEN = os.environ.get("FB_SHORT_ACCESS_TOKEN")
FB_LONG_ACCESS_TOKEN = os.environ.get("FB_LONG_ACCESS_TOKEN")
FB_APP_ID = os.environ.get("FB_APP_ID")
FB_APP_SECRET = os.environ.get("FB_APP_SECRET")
LTTK_GROUP_ID = '1488511748129645'
PAYLOAD = {
    'access_token': FB_LONG_ACCESS_TOKEN
}

POST_FIELDS = (
    'id,caption,created_time,description,from,link,message,'
    'message_tags,name,object_id,permalink_url,properties,'
    'shares,source,status_type,to,type,updated_time'
)
COMMENT_FIELDS = (
    'id,attachment,comment_count,created_time,from,'
    'like_count,message,message_tags,parent'
)
REACTION_FIELDS = (
    'id,name,type'
)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost/"
SPOTIFY_TOKEN = spotipy_util.prompt_for_user_token(
    '22gndvram3iydupmjvgg7fz2a', 'user-read-email', SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI)
SPOTIFY = spotipy.Spotify(auth=SPOTIFY_TOKEN)

class YoutubeTitleParser(object):
    """
    Parse a YouTube title to get artist name and song name
    Adopted from https://github.com/MrCorncob/Youtube-Title-Parser
    Not using as a package since its functionality is incomplete and
    it is not in active development anymore
    """
    song_name = None
    artist_name = None

    def __init__(self, title=None):
        self.song_name = ''
        self.artist_name = ''
        self.separators = SEPARATORS
        if title:
            self.split_artist_title(title)

    @staticmethod
    def _clean_fluff(string):
        result = re.sub(r'\s*\[[^\]]+\]$', '', string=string,
                        flags=re.IGNORECASE | re.MULTILINE)  # [whatever] at the end
        result = re.sub(r'^\s*\[[^\]]+\]\s*', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # [whatever] at the start
        result = re.sub(r'\s*\[\s*(M/?V)\s*\]', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # [MV] or [M/V]
        result = re.sub(r'\s*\(\s*(M/?V)\s*\)', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # (MV) or (M/V)
        result = re.sub(r'[\s\-–_]+(M/?V)\s*', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # MV or M/V at the end
        result = re.sub(r'(M/?V)[\s\-–_]+', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # MV or M/V at the start
        result = re.sub(r'\s*\([^\)]*\bver(\.|sion)?\s*\)$', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # (whatever version)
        result = re.sub(r'\s*[a-z]*\s*\bver(\.|sion)?$', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # ver. and 1 word before (no parens)
        result = re.sub(r'\(?\s*(of+icial\s*)?(music\s*)?video\)?', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # (official)? (music)? video
        result = re.sub(r'\s*(ALBUM TRACK\s*)?(album track\s*)', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # (ALBUM TRACK)
        result = re.sub(r'\s*\(?\s*of+icial\s*\)?', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # (official)
        result = re.sub(r'\s*\(\s*[0-9]{4}\s*\)', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # (1999)
        result = re.sub(r'\s+\(\s*(HD|HQ)\s*\)', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # HD (HQ)
        result = re.sub(r'[\s\-–_]+(HD|HQ)\s*', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE)  # HD (HQ)
        result = re.sub(r'\s*(of+icial\s*)?\(?(lyric)\)?(s)?\s*', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE) # Lyrics
        result = re.sub(r'\s*\(\s*\)\s*', '', string=result,
                        flags=re.IGNORECASE | re.MULTILINE) # ()

        return result

    @staticmethod
    def _clean_title(title):
        result = re.sub(r'/\s*\*+\s?\S+\s?\*+$/', '', title,
                        flags=re.IGNORECASE | re.MULTILINE)
        result = re.sub(r'/\s*video\s*clip/i', '', result,
                        flags=re.IGNORECASE | re.MULTILINE)  # **NEW**
        result = re.sub(r'/\s*video\s*clip/i', '', result,
                        flags=re.IGNORECASE | re.MULTILINE)  # video clip
        result = re.sub(r'/\s+\(?live\)?$/i', '', result,
                        flags=re.IGNORECASE | re.MULTILINE)  # live
        result = re.sub(r'/\(\s*\)/', '', result,
                        flags=re.IGNORECASE | re.MULTILINE)  # Leftovers after e.g. (official video)
        result = re.sub(r'/^(|.*\s)"(.*)"(\s.*|)$/', '$2', result,
                        flags=re.IGNORECASE | re.MULTILINE)
                        # Artist - The new "Track title" featuring someone
        result = re.sub(r'/^(|.*\s)\'(.*)\'(\s.*|)$/', '$2', result,
                        flags=re.IGNORECASE | re.MULTILINE)  # 'Track title'
        result = re.sub(r'/^[/\s,:;~\-–_\s"]+/', '', result,
                        flags=re.IGNORECASE | re.MULTILINE)  # trim starting white chars and dash
        result = re.sub(r'/[/\s,:;~\-–_\s"]+$/', '', result,
                        flags=re.IGNORECASE | re.MULTILINE)  # trim trailing white chars and dash
        return result

    @staticmethod
    def _clean_artist(artist):
        result = re.sub(r'/\s*[0-1][0-9][0-1][0-9][0-3][0-9]\s*/',
                        '', artist)  # date formats ex. 130624
        result = re.sub(r'/^[/\s,:;~\-–_\s"]+/', '', result,
                        flags=re.IGNORECASE | re.MULTILINE)  # trim starting white chars and dash
        result = re.sub(r'/[/\s,:;~\-–_\s"]+$/', '', result)  # trim starting white chars and dash

        return result

    def split_artist_title(self, title):
        parts = None
        title = self._clean_fluff(title)
        for separator in self.separators:
            if separator in title:
                parts = title.split('{}'.format(separator), 1)
                break

        if parts:
            self.song_name = self._clean_title(parts[1])
            self.artist_name = self._clean_artist(parts[0])
        else:
            self.song_name = title
            self.artist_name = ''

def refresh_access_token():
    """
    Refresh short access token
    """
    dotenvfile = find_dotenv()
    load_dotenv(dotenvfile)
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("ignore", ResourceWarning)
        dotenv.get_key(dotenvfile, "FB_LONG_ACCESS_TOKEN")
        warns = filter(lambda i: issubclass(i.category, UserWarning), warns)
        if warns:
            request_url = FB_URL + 'oauth/access_token'
            request_payload = {
                'grant_type': 'fb_exchange_token',
                'client_id': FB_APP_ID,
                'client_secret': FB_APP_SECRET,
                'fb_exchange_token': FB_SHORT_ACCESS_TOKEN
            }
            response = REQ_SESSION.get(request_url, params=request_payload).json()
            dotenvfile = find_dotenv()
            load_dotenv(dotenvfile)
            dotenv.set_key(dotenvfile, "FB_LONG_ACCESS_TOKEN", response['access_token'])
            PAYLOAD['access_token'] = dotenv.get_key(dotenvfile, "FB_LONG_ACCESS_TOKEN")

'''
TODO: refresh_long_token()
    A function to refresh the long term access token
    Current validity: 60 days
    UPDATE: Looks like there is currently no way to do this on the server-side.
    https://developers.facebook.com/docs/facebook-login/access-tokens/expiration-and-extension#refreshtokens
'''

def make_request(request_url, request_params):
    """
    Make a request to the Graph API, given the endpoint and params
    """
    response = REQ_SESSION.get(request_url, params=request_params)
    if response.status_code == 400:
        refresh_access_token()
        response = REQ_SESSION.get(request_url, params=request_params)
    return response.json()

def get_metadata(graph_object):
    """
    Get song metadata from Spotify
    """
    print(graph_object)
    if 'name' in graph_object:
        song_info = YoutubeTitleParser(graph_object['name'])
        print(song_info.artist_name, song_info.song_name)
        # response = SPOTIFY.search(q=graph_object['name'], type='track', limit=5)
        # print(response)

def parse_comments(comments, level):
    """
    Parse comments given comment id
    """
    for comment in comments:
        if level == 1:
            get_comments(comment['id'], level + 1)

def get_comments(graph_id, level):
    """
    Get the comments of a post with given id
    """
    request_url = FB_URL + graph_id + '/comments'
    request_params = PAYLOAD.copy()
    request_params['fields'] = COMMENT_FIELDS
    response = make_request(request_url, request_params)
    if response['data']:
        parse_comments(response['data'], level)
    while 'paging' in response:
        next_page_cursor = response['paging']['cursors']['after']
        comment_page_params = request_params.copy()
        comment_page_params['after'] = next_page_cursor
        response = make_request(request_url, comment_page_params)
        if response['data']:
            parse_comments(response['data'], level)
    return response

def get_reactions(graph_id):
    """
    Get the reactions to a post with given id
    """
    request_url = FB_URL + graph_id + '/reactions'
    request_params = PAYLOAD.copy()
    request_params['fields'] = REACTION_FIELDS
    response = make_request(request_url, request_params)
    while 'paging' in response:
        next_page_cursor = response['paging']['cursors']['after']
        comment_page_params = request_params.copy()
        comment_page_params['after'] = next_page_cursor
        response = make_request(request_url, comment_page_params)
    return response

def parse_post(post):
    """
    Parse the post for information
    """
    graph_id = post['id']
    # comments = get_comments(graph_id, 1)
    # reactions = get_reactions(graph_id)
    metadata = get_metadata(post)

def get_post(graph_id):
    """
    Get the post details for the given id
    """
    request_url = FB_URL + graph_id
    request_params = PAYLOAD.copy()
    request_params['fields'] = POST_FIELDS
    response = make_request(request_url, request_params)
    parse_post(response)

def parse_feed(feed):
    """
    Parse the posts in feed for information
    """
    for post in feed:
        get_post(post['id'])
        input()

def get_feed():
    """
    Fetch feed
    """
    request_url = FB_URL + LTTK_GROUP_ID + '/feed'
    response = make_request(request_url, PAYLOAD)
    parse_feed(response['data'])
    while 'paging' in response:
        next_page_url = response['paging']['next']
        response = make_request(next_page_url, PAYLOAD)
        parse_feed(response['data'])

def main():
    """
    Fetch posts from a Facebook group and populate in database
    """
    get_feed()

if __name__ == "__main__":
    main()
