import re
from music_metadata_extractor import SongData

def get_spotify_id(url):
    spotify_pattern = re.compile(
        r"""
        https?:\/\/open\.spotify\.com\/track\/(?P<id>[a-zA-Z0-9]+)
        """,
        re.VERBOSE
    )
    spotify_match = spotify_pattern.match(url)
    if spotify_match:
        return spotify_match.group("id")
    else:
        yt_pattern = re.compile(
            r"""
            (https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.
            (com|be)/(watch\?v=|embed/|v/|.+\?v=)?
            (?P<id>[A-Za-z0-9\-=_]{11})""",
            re.VERBOSE,
        )
        yt_match = yt_pattern.match(url)
        if(yt_match):
            data = SongData(url)
            if data.track:
                return data.track.provider_id
