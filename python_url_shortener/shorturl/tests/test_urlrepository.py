import pytest
from datetime import datetime, timedelta

from shorturl.model import OriginalUrl
from shorturl.urlrepository import InMemoryURLRepository, NoneKeyError


def test_none_when_shorturl_non_present():
    """ getting a non existing short url returns None """
    repository = InMemoryURLRepository()
    assert repository.get("a-short-url") is None


def test_put_none_short_url():
    """  putting a None short url raises a NoneKeyError """
    repository = InMemoryURLRepository()
    with pytest.raises(NoneKeyError):
        repository.put(None, "url")


def test_url_updated_when_putting_same_key_different_url():
    """ updating a short url works """
    repository = InMemoryURLRepository()
    short_url = "short"
    original_url1 = OriginalUrl("www.first.com")
    original_url2 = OriginalUrl("www.second.com", datetime.now())
    repository.put(short_url, original_url1)
    repository.put(short_url, original_url2)
    assert len(repository.url_map) == 1
    assert repository.get(short_url) is original_url2


def test_put_and_get_shorturl():
    """ putting and getting a short url works """
    repository = InMemoryURLRepository()
    short_url = "short"
    original_url = OriginalUrl("www.url.com/rr")
    repository.put(short_url, original_url)
    assert repository.get(short_url) is original_url


def test_delete_non_existing_shorturl_raises_keyerror():
    """ deleting a non existing short url raises a KeyError """
    repository = InMemoryURLRepository()
    with pytest.raises(KeyError):
        repository.delete("a-short-url")


def test_delete_existing_shorturl():
    """ short urls can be deleted """
    repository = InMemoryURLRepository()
    short_url = "short"
    original_url = OriginalUrl("www.url.com/rr")
    repository.put(short_url, original_url)
    repository.delete(short_url)
    assert len(repository.url_map) == 0


def test_delete_older_than():
    """ original urls with timestamp older than given are deleted """
    repository = InMemoryURLRepository()
    now = datetime.now()
    a_day = timedelta(days=1)
    a_year = timedelta(days=365)
    short_url, short_url1, short_url2 = "short", "short1", "short2"
    original_url = OriginalUrl("www.url.com")
    original_url_recent = OriginalUrl("www.url.com", now)
    original_url_old = OriginalUrl("www.old.com", now - a_year)
    repository.put(short_url, original_url)
    repository.put(short_url1, original_url_recent)
    repository.put(short_url2, original_url_old)
    a_day_ago = now - a_day
    repository.delete_older_than(a_day_ago)

    assert len(repository.url_map) == 2
    for _, original_url in repository.url_map.items():
        assert original_url.timestamp is None or original_url.timestamp > a_day_ago
