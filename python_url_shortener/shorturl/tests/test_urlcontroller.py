from unittest.mock import MagicMock
from unittest import mock

import pytest

from shorturl.urlcontroller import ShortUrlController, UrlGenerationTimeoutException
from shorturl.model import OriginalUrl


@mock.patch('shorturl.urlrepository.InMemoryURLRepository')
def test_short_url_not_found(mock_repo):
    """ Return None when short url not found """
    mock_repo.get = MagicMock(return_value=None)
    mock_generate = MagicMock
    controller = ShortUrlController(mock_repo, mock_generate)

    assert controller.get_original_url("shorturl") is None


@mock.patch('shorturl.urlrepository.InMemoryURLRepository')
def test_get_original_url_for_existing_short_url(mock_repo):
    """ get_original_url for an existing short url works """
    original_url = OriginalUrl("www.ibm.com")
    mock_repo.get = MagicMock(return_value=original_url)
    mock_generate = MagicMock
    controller = ShortUrlController(mock_repo, mock_generate)

    assert controller.get_original_url("shorturl") is original_url


@mock.patch('shorturl.urlgenerator.generate_url')
@mock.patch('shorturl.urlrepository.InMemoryURLRepository')
def test_shorten_url(mock_repo, mock_generate):
    """ a url is shortened and the result is correctly prefixed """
    url = "www.ibm.com"
    short_url = "yyy"
    mock_generate.return_value = short_url
    mock_repo.get = MagicMock(return_value=None)
    controller = ShortUrlController(mock_repo, mock_generate)

    shortened_url = controller.shorten_url(url)

    _assert_put_call_args(mock_repo, short_url, url)
    assert shortened_url.short_url == "http://www.your_service.com/{}".format(short_url)


@mock.patch('shorturl.urlgenerator.generate_url')
@mock.patch('shorturl.urlrepository.InMemoryURLRepository')
def test_shorten_url_generates_again_when_existing(mock_repo, mock_generate):
    """ a new short url is generated if the current is already mapped """
    url = "www.ibm.com"
    shortened_url1 = "sdede"
    shortened_url2 = "dvdfs"
    mock_generate.side_effect = [shortened_url1, shortened_url2]
    mock_repo.get = MagicMock(side_effect=[OriginalUrl("existing"), None])
    controller = ShortUrlController(mock_repo, mock_generate)

    shortened_url = controller.shorten_url(url)

    _assert_put_call_args(mock_repo, shortened_url2, url)
    assert shortened_url.short_url == "http://www.your_service.com/{}".format(shortened_url2)


@mock.patch('shorturl.urlgenerator.generate_url')
@mock.patch('shorturl.urlrepository.InMemoryURLRepository')
def test_shorten_url_timouts_after_some_time_if_generated_urls_exist(mock_repo, mock_generate):
    """ a UrlGenerationTimeoutException is generated if all the generated short urls exist """
    url = "www.ibm.com"
    shortened_url1 = "sdede"
    shortened_url2 = "xaaa3"
    shortened_url3 = "cdece"
    mock_generate.side_effect = [shortened_url1, shortened_url2, shortened_url3]
    mock_repo.get = MagicMock(side_effect=[OriginalUrl("existing"), OriginalUrl("existing"), OriginalUrl("existing")])
    controller = ShortUrlController(mock_repo, mock_generate)

    with pytest.raises(UrlGenerationTimeoutException):
        controller.shorten_url(url)


def _assert_put_call_args(mock_repo, short_url, url):
    """ assert put is called on the given repo mock with the given arguments """
    call = mock_repo.put.mock_calls[0]
    f, args, kwargs = call
    (short_url_arg, original_url_arg) = args
    assert short_url_arg == short_url
    assert original_url_arg.url == url
