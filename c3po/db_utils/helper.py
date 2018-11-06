import dateutil.parser
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

import db_utils.db as db
import db_utils.parse_metadata as pm

def add_post_to_db(parsed_post):
    # user_id = parsed_post['post']['from']['id']
    # user_name = parsed_post['post']['from']['name']
    # user_id = 1
    user_name = "LTTKGP member"
    db_user = db.User(user_name=user_name)
    post_id = parsed_post['post']['id']
    post_time = dateutil.parser.parse(parsed_post['post']['created_time'])
    db_post = db.Post(post_id=post_id, post_time=post_time)
    db_user.posts.append(db_post)
    song_title, genre_name, artist_name = pm.parse_musixmatch(parsed_post['metadata']['musixmatch'])
    sp_song_title, sp_artist_name = pm.parse_spotify(parsed_post['metadata']['spotify'])
    if song_title is None:
        song_title = sp_song_title
    if artist_name is None:
        artist_name = sp_artist_name
    db_song = db.Song(song_title=song_title)
    db_genre = db.Genre(genre_name=genre_name)
    db_artist = db.Artist(artist_name=artist_name)
    db_song.artists.append(db_artist)
    db_song.genres.append(db_genre)
    link_type = 'yt'
    link_value = parsed_post['post']['link']
    db_link = db.Link(link_type=link_type, link_value=link_value)
    db_song.links.append(db_link)
    db_link.posts.append(db_post)
    db_session = db.Session()
    if not db_session.query(exists().where(db.User.user_id==db_user.user_id)).scalar():
        print("AAAAAAAAAAAAAAAAAAAAAA")
        db_session.add(db_user)
    if not db_session.query(exists().where(db.Post.post_id==db_post.post_id)).scalar():
        print("BBBBBBBBBBBBBBBBBBBBBB")
        db_session.add(db_post)
    if not db_session.query(exists().where(db.Song.song_id==db_song.song_id)).scalar():
        print("CCCCCCCCCCCCCCCCCCCCCC")
        db_session.add(db_song)
    if not db_session.query(exists().where(db.Genre.genre_id==db_genre.genre_id)).scalar():
        print("DDDDDDDDDDDDDDDDDDDDDD")
        db_session.add(db_genre)
    if not db_session.query(exists().where(db.Artist.artist_id==db_artist.artist_id)).scalar():
        print("EEEEEEEEEEEEEEEEEEEEEE")
        db_session.add(db_artist)
    if not db_session.query(exists().where(db.Link.link_id==db_link.link_id)).scalar():
        print("FFFFFFFFFFFFFFFFFFFFFF")
        db_session.add(db_link)
    db_session.commit()
    try:
        test_post = db_session.query(db.User).one()
        print(test_post)
    except MultipleResultsFound as e:
        print(e)
    except NoResultFound as e:
        print(e)
    db_session.close()
