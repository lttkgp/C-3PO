from abc import ABC, abstractmethod
from urllib.parse import urlparse
from youtube import YouTube


class LinkResolver(object):
    youtube_domains = [
        'www.youtube.com', 'm.youtube.com', 'youtube.com', 'youtu.be'
    ]

    @staticmethod
    def resolve(self, link):
        domain = urlparse(link).netloc
        if domain in self.youtube_domains:
            return YouTube()


class metadata(ABC):
    def __init__(self):
        super().__init__()
