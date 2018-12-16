import json
import os
import warnings
from os.path import abspath, dirname, join

import dotenv
import requests
from dotenv import find_dotenv, load_dotenv
# from youtube_music_metadata import get_metadata

import constants

DOTENV_PATH = join(dirname(dirname(dirname(abspath(__file__)))), '.env')
load_dotenv(DOTENV_PATH)

REQ_SESSION = requests.Session()
FB_URL = 'https://graph.facebook.com/' + constants.FACEBOOK_API_VERSION + '/'
FB_SHORT_ACCESS_TOKEN = os.environ.get("FB_SHORT_ACCESS_TOKEN")
FB_LONG_ACCESS_TOKEN = os.environ.get("FB_LONG_ACCESS_TOKEN")
FB_APP_ID = os.environ.get("FB_APP_ID")
FB_APP_SECRET = os.environ.get("FB_APP_SECRET")
GROUP_ID = constants.FACEBOOK_GROUP_ID
PAYLOAD = {'access_token': FB_LONG_ACCESS_TOKEN}
COMMENT_LOCKDOWN = constants.FACEBOOK_COMMENT_LOCKDOWN
REACTION_LOCKDOWN = constants.FACEBOOK_REACTION_LOCKDOWN


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
            response = REQ_SESSION.get(
                request_url, params=request_payload).json()
            dotenvfile = find_dotenv()
            load_dotenv(dotenvfile)
            print(response)
            dotenv.set_key(dotenvfile, "FB_LONG_ACCESS_TOKEN",
                           response['access_token'])
            PAYLOAD['access_token'] = dotenv.get_key(dotenvfile,
                                                     "FB_LONG_ACCESS_TOKEN")


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


def parse_comments(response, level, comments):
    """
    Parse comments given comment id
    """
    for comment in response:
        comments.append(comment)
        if level == 1:
            get_comments(comment['id'], level + 1, comments)


def get_comments(graph_id, level, comments):
    """
    Get the comments of a post with given id
    """
    request_url = FB_URL + graph_id + '/comments'
    request_params = PAYLOAD.copy()
    request_params[
        'fields'] = 'comments.summary(true){' + constants.FACEBOOK_COMMENT_FIELDS + '}'
    response = make_request(request_url, request_params)
    if response['data']:
        parse_comments(response['data'], level, comments)
    while 'paging' in response:
        next_page_cursor = response['paging']['cursors']['after']
        comment_page_params = request_params.copy()
        comment_page_params['after'] = next_page_cursor
        response = make_request(request_url, comment_page_params)
        if response['data']:
            parse_comments(response['data'], level, comments)


def get_reactions(graph_id):
    """
    Get the reactions to a post with given id
    """
    request_url = FB_URL + graph_id + '/reactions'
    request_params = PAYLOAD.copy()
    request_params[
        'fields'] = 'reactions.summary(true){' + constants.FACEBOOK_REACTION_FIELDS + '}'
    response = make_request(request_url, request_params)
    reactions = []
    reactions += response['data']
    while 'paging' in response:
        next_page_cursor = response['paging']['cursors']['after']
        comment_page_params = request_params.copy()
        comment_page_params['after'] = next_page_cursor
        response = make_request(request_url, comment_page_params)
        reactions += response['data']
        return reactions


def build_feed_request():
    request_url = FB_URL + GROUP_ID + '/feed'
    request_params = PAYLOAD.copy()
    request_params['fields'] = constants.FACEBOOK_POST_FIELDS
    request_params[
        'fields'] = request_params['fields'] + ',reactions.summary(true){'
    request_params['fields'] = request_params[
        'fields'] + constants.FACEBOOK_REACTION_FIELDS + '}'
    request_params[
        'fields'] = request_params['fields'] + ',comments.summary(true){'
    request_params['fields'] = request_params[
        'fields'] + constants.FACEBOOK_COMMENT_FIELDS + '}'
    return request_url, request_params


def get_feed(next_link=""):
    """
    Fetch feed
    """
    if not next_link:
        request_url, request_params = build_feed_request()
        response = make_request(request_url, request_params)
        return response['data'], response['paging']['next']
