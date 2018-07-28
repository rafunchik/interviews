import unittest

import shorturl

import os
import tempfile

import pytest

from flaskr import flaskr

@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()

    with flaskr.app.app_context():
        flaskr.init_db()

    yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])

class ShorturlTestCase(unittest.TestCase):

    def setUp(self):
        self.app = shorturl.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to url_shortener', rv.data.decode())


if __name__ == '__main__':
    unittest.main()



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
#     "should return 404 upon a GET with a not found short url" >> {
#       val request = Request[IO](Method.GET, Uri.uri("/unknown_short_url"))
#
#       checkStatus(request, Status.NotFound)
#     }
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
