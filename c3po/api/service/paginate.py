from urllib.parse import  urlparse , urlunparse, parse_qs
from collections import OrderedDict
from urllib.parse import urlencode

def get_paginated_response(posts, url, start=0, limit=24):
    total = len(posts)
    if limit > total:
        return None
    response = {}
    response['start'] = start
    response['limit'] = limit
    response['total'] = total

    if start + limit > total:
        response['next'] = ''
    else:
        next_start = start + limit
        response['next'] = _build_url(url, start + limit, limit)
    
    response['posts'] = posts[start: start + limit]
    return response

def _build_url(url, start, limit):
    base_url = url[:url.find('?') + 1]
    query_params = OrderedDict(parse_qs(urlparse(url).query))

    new_query_params = {}
    for key in query_params.keys():
        if key == 'start':
            new_query_params[key] = str(start)
        elif key == 'limit':
            new_query_params[key] = str(limit)
        else:
            new_query_params[key] =query_params[key][0]
    return base_url + urlencode(new_query_params)

    