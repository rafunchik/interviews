import unittest

from shorturl import app


import os
import tempfile

import pytest

from flask import request, jsonify

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
                           headers={'content-type':'application/json'})
    assert response.status_code == 400


def test_invalid_json(client):
    """Test status code 400 from improper JSON on post to raw"""
    response = client.post(SHORTEN_URL_ENDPOINT,
                           data='{"not url": "www.bbc.com"}',
                           headers={'content-type':'application/json'})
    assert response.status_code == 400


def test_wrong_url_format_json(client):
    """Test status code 400 from improper JSON url on post to raw"""
    response = client.post(SHORTEN_URL_ENDPOINT,
                           data='{"url": "::/www.bbc.com"}',
                           headers={'content-type':'application/json'})
    assert response.status_code == 400


def test_shorten_url_successfully(client):
    """ A well formatted URL is shortened fine with a 201 status code"""
    response = client.post(SHORTEN_URL_ENDPOINT,
                           data='{"url": "www.helloworld.com"}',
                           headers={'content-type':'application/json'})
    json_data = response.get_json()
    assert response.status_code == 201
    # assert "xx" == json_data['shortened_url']





# class ShorturlTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.app = shorturl.app.test_client()
#
#     def test_index(self):
#         rv = self.app.get('/')
#         self.assertIn('Welcome to url_shortener', rv.data.decode())
#
#
# if __name__ == '__main__':
#     unittest.main()



#   "ShortUrlApp" >> {
#     "should return 201 upon a POST to shorten_url with a valid JSON body" >> {
#       val request =  Request[IO](method = Method.POST, uri = Uri.uri("/shorten_url"))
#         .withBody(ValidURLJSON)
#         .unsafeRunSync()
#       val response = new ShortUrlService[IO].service.orNotFound(request).unsafeRunSync()
#       response.status must beEqualTo(Status.Created)
#       val shortUrl = response.as[ShortenedUriResponse].unsafeRunSync()
#       shortUrl.shortened_url must startWith("http://www.your_service.com/")
#     }
#
#     "should return 400 upon a POST to shorten_url with an invalid JSON body" >> {
#       val request = Request[IO](method = Method.POST, uri = Uri.uri("/shorten_url"))
#         .withBody(InvalidJSON)
#         .unsafeRunSync()
#
#       checkStatus(request, Status.BadRequest)
#     }
#
#     "should return 400 upon a POST to shorten_url with a malformed URL in the JSON body" >> {
#       val request = Request[IO](method = Method.POST, uri = Uri.uri("/shorten_url"))
#         .withBody(MalformedURLJSON)
#         .unsafeRunSync()
#
#       checkStatus(request, Status.BadRequest)
#       checkBody(request, "DecodingFailure at .url: Uri")
#     }
#
#     "should return 400 upon a POST to shorten_url with a malformed JSON body" >> {
#       val request = Request[IO](method = Method.POST, uri = Uri.uri("/shorten_url"))
#         .withBody(MalformedJSON)
#         .unsafeRunSync()
#
#       checkStatus(request, Status.BadRequest)
#     }
#
#     "should return 307 upon a GET with a found short url" >> {
#       val postRequest =  Request[IO](method = Method.POST, uri = Uri.uri("/shorten_url"))
#         .withBody(ValidURLJSON)
#         .unsafeRunSync()
#       val shortUrlService = new ShortUrlService[IO]
#       val postResponse = shortUrlService.service.orNotFound(postRequest).unsafeRunSync()
#       val shortUrl = postResponse.as[ShortenedUriResponse].unsafeRunSync()
#
#       val getRequest = Request[IO](Method.GET, Uri.fromString(s"/${shortUrl.shortSuffix}").right.get)
#       val getResponse = shortUrlService.service.orNotFound(getRequest).unsafeRunSync()
#
#       getResponse.status must beEqualTo(Status.TemporaryRedirect)
#       getResponse.headers.get(CaseInsensitiveString("Location")) must beSome[Header](Header("Location", "www.helloworld.com"))
#     }
#

#
#     "should return 404 upon a POST to a wrong URL" >> {
#       val request = Request[IO](Method.POST, Uri.uri("/shorten_url/xxx"))
#
#       checkStatus(request, Status.NotFound)
#     }
#
#     "should return 500 upon an application error" >> {
#       implicit val clock: Clock = Clock.systemUTC()
#       val request = Request[IO](Method.POST, Uri.uri("/shorten_url"))
#         .withBody(ValidURLJSON)
#         .unsafeRunSync()
#       val mockController = mock[ShortUrlController]
#       mockController.shortenUrl(any())(any()) returns UrlGenerationTimeoutException("Time out").asLeft
#
#       val response = new ShortUrlService[IO].defineService(mockController).orNotFound(request).unsafeRunSync()
#
#       response.status must beEqualTo(Status.InternalServerError)
#     }
#   }
#
#   private def checkStatus(request: Request[IO], status: Status) = {
#     val response = new ShortUrlService[IO].service.orNotFound(request).unsafeRunSync()
#     response.status must beEqualTo(status)
#   }
#   //TODO merge methods
#   private def checkBody(request: Request[IO], body: String) = {
#     val response = new ShortUrlService[IO].service.orNotFound(request).unsafeRunSync()
#     response.as[String].unsafeRunSync() must beEqualTo(body)
#   }
# }
#
# object ShortUrlServiceSpec {
#   val ValidURLJSON = json"""{"url": "www.helloworld.com"}"""
#   val InvalidJSON = json"""{"not url": "www.helloworld.com"}"""
#   val MalformedURLJSON = json"""{"url": ":::www.helloworld.com"}"""
#   val MalformedJSON = "\"url\": \"www.helloworld.com\"}}}}"
# }
