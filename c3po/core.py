"""
Core script. Structure to be changed later.
"""
import os
from os.path import join
import dotenv
from dotenv import find_dotenv, load_dotenv
import requests

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

def refresh_short_token():
    """
    Refresh short access token
    """
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
'''

def get_feed():
    """
    Fetch feed
    """
    request_url = FB_URL + LTTK_GROUP_ID + '/feed'
    response = REQ_SESSION.get(request_url, params=PAYLOAD)
    if response.status_code == 400:
        refresh_short_token()
    print(response.json())
    return response.json()

def main():
    """
    Fetch posts from a Facebook group and populate in database
    """
    get_feed()

if __name__ == "__main__":
    main()
