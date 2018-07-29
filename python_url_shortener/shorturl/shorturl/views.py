from flask import request, abort, redirect, url_for, jsonify
from urllib.parse import urlparse

from shorturl import app


def _get_url_to_be_shortened(request):
    """ Tries to parse a url from the url field, raises an exception if not able to """

    json_data = request.get_json()
    result = urlparse(json_data['url'])
    print(result.geturl())
    return result.geturl()

@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    """ Accepts a POST to the shorten_url endpoint, with a valid JSON url object, e.g.
    curl -H "Content-Type: application/json" -d '{"url": "www.hello.com"}' http://localhost:8080/shorten_url
    if successful, generates, saves and returns a 201 (created) response with the new shortened url, otherwise
    returns a 400, 405 or 500, depending on the error. """

    if request.method == 'POST':
        try:
            url = _get_url_to_be_shortened(request)
        except:
            return "malformed url in json request", 400
        short_url = con_shorten_url(url)
        return jsonify({'shortened_url': short_url}), 201


# TODO move to controller
def get_original_url(short_url):
    return None


def con_shorten_url(url):
    "url"


@app.route('/<short_url>', methods=['GET'])
def redirect_to_original_url(short_url):
    """ Accepts a GET to the root endpoint, with a short_url path parameter, e.g.
    curl -i localhost:8080/BdhHbLINOA,
    if the short url is found, redirects to its original url, if not, a 404 (not found) is returned """

    try:
        original_url = get_original_url(short_url)
    except:
        return "Not found", 404
    # app.logger.warning('sample message')
    if original_url:
        return redirect(original_url), 307  # url_for('login')) # return '', 201
    else:
        return "Not found", 404


# case
# GET -> Root / shortUrl = >
#
# shortUrlController.getOriginalUrl(shortUrl)
# match
# {
#     case
# Some(urlDTO) = > TemporaryRedirect(Location(urlDTO.url))
# case
# _ = > NotFound("Short URL not found")
# }
#

# case
# request @ POST -> Root / "shorten_url" = >
# import org.http4s.circe.CirceEntityDecoder._
#
# val
# response = request.as[OriginalUrlRequest].attempt.flatMap
# {
#     case
# Right(originalUrl) = > {
#     shortUrlController.shortenUrl(originalUrl.url)
# match
# {
#     case
# Right(shortenedUrl) = > createdSuccessfully(shortenedUrl)
# case
# Left(e) = > internalServerError(e)
# }
# }
# case
# Left(error) = > badRequest(error)
# }
#
#
# response
#


# case(PUT | PATCH | DELETE) = > MethodNotAllowed("Only GET with a url param and POST to shorten_url allowed")