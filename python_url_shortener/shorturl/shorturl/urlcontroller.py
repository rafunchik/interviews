from datetime import datetime
from shorturl.model import OriginalUrl


class UrlGenerationTimeoutException(Exception):
    """ Exception representing a timeout when generating a short url """
    pass


class ShortUrlDTO:
    """ Data transfer object for the short url, which prepends the service name to the short url """
    def __init__(self, short_url):
        self._short_url = short_url

    @property
    def short_url(self):
        """
        :return: short url prepended by service name (http://www.your_service.com)
        """
        return "http://www.your_service.com/{}".format(self._short_url)


class ShortUrlController:
    """ Short url controller, responsible for the handling of urls """

    URL_GENERATION_TIMEOUT = 3

    def __init__(self, url_repository, generate_short_url):
        self.url_repository = url_repository
        self.generate_short_url_fn = generate_short_url

    def get_original_url(self, short_url):
        """ Attempts to retrieve the original url corresponding to this short url
        :param short_url: short_url string
        :return: Original url or None, if not found
        """
        return self.url_repository.get(short_url)

    def shorten_url(self, url):
        """ Attempts to shorten a given url (timeouts if not possible), storing it along the original url and timestamp

        :param url: a valid url string
        :return: ShortUrlDTO with the shortened url\
        :raise: UrlGenerationTimeoutException if couldn't generate a new short url in time
        """
        for _ in range(self.URL_GENERATION_TIMEOUT):
            short_url = self.generate_short_url_fn(url)
            if not self.url_repository.get(short_url):
                original_url = OriginalUrl(url=url, timestamp=datetime.now())
                self.url_repository.put(short_url, original_url)
                return ShortUrlDTO(short_url)
        raise UrlGenerationTimeoutException("Took too long to generate a non existing short url")
