"""
Core script. Structure to be changed later.
"""
import os
from os.path import join
import warnings
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
POST_FIELDS = (
    'id,caption,created_time,description,from,link,message,'
    'message_tags,name,object_id,permalink_url,properties,'
    'shares,source,status_type,to,type,updated_time'
    )

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

def get_post(graph_id):
    """
    Get the post details for the given id
    """
    request_url = FB_URL + graph_id
    request_params = PAYLOAD
    request_params['fields'] = POST_FIELDS
    response = make_request(request_url, request_params)
    print(response)

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
