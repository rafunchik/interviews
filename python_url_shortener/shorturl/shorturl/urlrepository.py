from abc import ABC, abstractmethod


class NoneKeyError(Exception):
    """
    """
    pass


class URLRepository(ABC):
    """ Abstract short url/original url repository """

    @abstractmethod
    def get(self, short_url):
        pass

    @abstractmethod
    def put(self, short_url, original_url):
        pass

    @abstractmethod
    def delete(self, short_url):
        pass

    @abstractmethod
    def delete_older_than(self, timestamp):
        pass


class InMemoryURLRepository(URLRepository):
    """ A short url/original url URLRepository in memory, the key can be a short url string or hash,
      and the values OriginalUri instances """

    def __init__(self):
        self.url_map = dict()

    def get(self, short_url):
        """ Retrieve mapped OriginalUri

        :param short_url: string
        :return: mapped OriginalUri or None if not found
        """
        return self.url_map.get(short_url)

    def put(self, short_url, original_url):
        """ Add or update short url/original url mapping

        :param short_url: string, if None a NoneKeyError is raised
        :param original_url: OriginalUri
        """
        if short_url is None:
            raise NoneKeyError("Short url can not be None")
        self.url_map[short_url] = original_url

    def delete(self, short_url):
        """ Delete short url from repository

        :param short_url: string
        :raise: KeyError is short_url not found
        """
        del self.url_map[short_url]

    def delete_older_than(self, timestamp):
        """ Delete short urls with OriginalUri values, where the value's timestamp is defined and is older
         or same as timestamp

        :param timestamp: datetime
        """
        recent = {k: v for k, v in self.url_map.items() if v.timestamp is None or v.timestamp > timestamp}
        self.url_map = recent
