from shorturl.urlgenerator import generate_url


def test_short_url_generates_unique_with_default_length():
    """ Consecutively generates different short urls with a default length of 10 """
    short_url = "xxx"
    urls = frozenset([generate_url(short_url), generate_url(short_url), generate_url(short_url)])
    assert len(urls) == 3
    for url in urls:
        assert len(url) == 10


def test_short_url_generates_urls_with_given_length():
    """ Generates a short url with a given length of 5 """
    short_url = "xxx"
    url = generate_url(short_url, 5)
    assert len(url) == 5
