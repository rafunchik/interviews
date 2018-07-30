import pytest

from shorturl import app

SHORTEN_URL_ENDPOINT = '/shorten_url'


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_root_url_produces_not_found(client):
    """ A GET to / should return 404 """
    # with app.test_client() as client:
    response = client.get('/')
    assert response.status_code == 404


def test_get_not_found_url(client):
    """ A GET to a not found short url should return 404 """
    # with app.test_client() as client:
    response = client.get('/unknown_short_url')
    assert response.status_code == 404


def test_malformed_json(client):
    """Test status code 400 from malformed JSON on post to raw"""
    response = client.post(SHORTEN_URL_ENDPOINT,
                           data="This isn't a json... it's a string!",
                           headers={'content-type': 'application/json'})
    assert response.status_code == 400


def test_invalid_json(client):
    """Test status code 400 from improper JSON on post to raw"""
    response = client.post(SHORTEN_URL_ENDPOINT,
                           data='{"not url": "www.bbc.com"}',
                           headers={'content-type': 'application/json'})
    assert response.status_code == 400


def test_wrong_url_format_json(client):
    """Test status code 400 from improper JSON url on post to raw"""
    response = client.post(SHORTEN_URL_ENDPOINT,
                           data='{"url": "::/www.bbc.com"}',
                           headers={'content-type': 'application/json'})
    assert response.status_code == 400


def test_shorten_url_successfully(client):
    """ A well formatted URL is shortened fine with a 201 status code"""
    response = client.post(SHORTEN_URL_ENDPOINT,
                           data='{"url": "www.helloworld.com"}',
                           headers={'content-type': 'application/json'})
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['shortened_url'].startswith("http://www.your_service.com/")


def test_redirect_when_found_short_url(client):
    """ Redirect with a 307 upon a GET with a short url mapped to an original url """
    response = client.post(SHORTEN_URL_ENDPOINT,
                           data='{"url": "www.helloworld.com"}',
                           headers={'content-type': 'application/json'})
    json_data = response.get_json()
    short_url = json_data['shortened_url'].split("http://www.your_service.com/")[1]
    response = client.get('/{}'.format(short_url))
    assert response.status_code == 307
    assert response.headers['Location'] == "http://www.helloworld.com"
