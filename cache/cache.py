import datetime


class Cache:
    """Cache class with two method for adding and checking items."""

    def __init__(self):
        self.memory = {}

    def add_key(self, key, value):
        """Method for adding item to dictionary.
        :param key: dictionary key,
        :param value: dictionary value,
        """
        self.memory[key] = [datetime.datetime.now(), value]
        return self.memory

    def check_key(self, key, minutes):
        """method for checking dictionary keys according to creation time and checking time.
        :param key: dictionary key .
        :param minutes: time for which data is to be cached.
        """
        current_time = datetime.datetime.now()

        search_key = key if key in self.memory.keys() else None
        if search_key:
            time_cached = self.memory[key][0]
            time_difference = current_time - time_cached
            if time_difference < datetime.timedelta(minutes=minutes):
                img_url = self.memory[key][1]
                return img_url
            else:
                return
