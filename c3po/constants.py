# API version
FACEBOOK_API_VERSION = "v6.0"

# Group information
FACEBOOK_GROUP_ID = "1488511748129645"

# Fields to fetch from API
FACEBOOK_POST_FIELDS = (
    "id,created_time,from,link,message,message_tags,"
    "name,object_id,permalink_url,properties,"
    "shares,source,status_type,type,updated_time"
)
FACEBOOK_COMMENT_FIELDS = (
    "id,attachment,comment_count,created_time,from,"
    "like_count,message,message_tags,parent"
)
FACEBOOK_COMMENT_LOCKDOWN = True
FACEBOOK_REACTION_FIELDS = "id,name,type"
FACEBOOK_REACTION_LOCKDOWN = True

# Feed update check
FEED_FIRST_TIME = False
FEED_CHECK_DEPTH = 2500
