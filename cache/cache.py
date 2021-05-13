import datetime as dt
from dataclasses import dataclass


@dataclass
class Cache:
    dimensions: str
    time_cached: dt.datetime
    url: str


class CacheMemory:
    """CacheMemory class with two method for adding and checking items."""

    def __init__(self, memory=None):
        if memory is None:
            self.memory = []
        else:
            self.memory = memory

    def add_cache(self, dimensions, img_url):
        """Method for adding item to dictionary.
        :param dimensions: dimensions of image
        :param img_url: image url
        """
        cache = Cache(dimensions=dimensions, time_cached=dt.datetime.now(), url=img_url)
        self.memory.append(cache)
        return self.memory

    def check_cache(self, dimensions, minutes):
        """Method for checking dictionary keys according to creation time and checking time.
        :param dimensions: dimensions which is being checked
        :param minutes: time for which data is to be cached in minutes.
        """
        index = 0
        for cache in self.memory:
            time_difference = dt.datetime.now() - cache.time_cached
            if cache.dimensions == dimensions:
                if time_difference < dt.timedelta(minutes=minutes):
                    cache.time_cached = dt.datetime.now()
                    return cache.url
            else:
                if time_difference > dt.timedelta(minutes=minutes):
                    del self.memory[index]
            index += 1
