class OriginalUrl:
    """ Model representing the original url to be shortened plus optional timestamp (a datetime, defaults to None) """

    def __init__(self, url, timestamp=None):
        self.url = url
        self.timestamp = timestamp
