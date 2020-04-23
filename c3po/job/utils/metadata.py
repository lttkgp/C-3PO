from c3po.db.dao import user, link, song, artist, genre
from c3po.db.common.base import session_factory
from datetime import datetime
from music_metadata_extractor import SongData

session = session_factory()

class Metadata:
    def __init__(self, url):
        self.url = url
        self.data = SongData(url)

    def insert(self):
        new_link = self._insert_link(self.url)
        if(new_link):
            new_song = self._insert_song(self.data.track)
            new_link.song_id = new_song.id
            for artist_data in self.data.artists:
                new_artist = self._insert_artist(artist_data)
                new_artist_song = artist.ArtistSong(new_artist, new_song)
                session.add(new_artist_song)
        session.commit()

    def _insert_link(self, url):
        query = list(session.query(link.Link).filter(link.Link.url == url))
        if(not query):
            temp_link = link.Link(url, 0)
            temp_link.post_count = 1
            session.add(temp_link)
            session.commit()
            return temp_link
        else:
            query[0].post_count += 1
            session.commit()
            return None

    def _insert_song(self, track_data):
        new_song = song.Song(
            track_data.name, 
            datetime.strptime(track_data.year, "%Y-%m-%d"), 
            track_data.explicit, 
            track_data.popularity, 
            track_data.image_id, 
            track_data.is_cover,
            track_data.original_id
        )
        session.add(new_song)
        session.commit()
        return new_song

    def _insert_artist(self, artist_data):
        query = list(session.query(artist.Artist).filter(artist.Artist.name == artist_data.name))
        if(not query):
            new_artist = artist.Artist(artist_data.name, artist_data.image_id)
            session.add(new_artist)
            session.commit()
            return new_artist
        return query.first()

    def _insert_genre(self, genre_data):
        query = list(session.query(genre.Genre).filter(genre.Genre.name == genre_data.name))
        if(not query):
            temp_genre = genre.Genre(genre_data.name)
            session.add(temp_genre)
            session.commit()
            return temp_genre
        return query.first()
