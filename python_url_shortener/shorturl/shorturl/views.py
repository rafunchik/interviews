from flask import request, redirect, jsonify
import validators

from shorturl import app
from shorturl.urlcontroller import ShortUrlController, UrlGenerationTimeoutException
from shorturl.urlgenerator import generate_url
from shorturl.urlrepository import InMemoryURLRepository


def _validate_url_to_be_shortened(in_request):
    """ Tries to parse a url from the url field, returns a @type: ValidationFailure which
    evaluates to False if not able to validate it
    :param in_request: request
    :return: url string upon validation, or a @type ValidationFailure upon failure """

    json_data = in_request.get_json()
    url = json_data['url']
    if validators.url(url) or validators.url("http://" + url):
        return url


def _initialize_controller():
    repository = InMemoryURLRepository()
    return ShortUrlController(url_repository=repository, generate_short_url=generate_url)


SHORT_URL_CONTROLLER = _initialize_controller()


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    """ Accepts a POST to the shorten_url endpoint, with a valid JSON url object, e.g.
    curl -H "Content-Type: application/json" -d '{"url": "www.hello.com"}' http://localhost:8080/shorten_url
    :return if successful, generates, saves and returns a 201 (created) response with the new shortened url, prefixed
    with the service name (http://www.your_service.com) otherwise returns a 400, 405 or 500, depending on the error. """

    if request.method == 'POST':
        try:
            url = _validate_url_to_be_shortened(request)
        except KeyError:
            return "malformed url in json request", 400
        if not url:
            return "malformed url in json request", 400
        try:
            short_url = SHORT_URL_CONTROLLER.shorten_url(url).short_url
        except UrlGenerationTimeoutException:
            return "could not generate a valid short url", 500
        return jsonify({'shortened_url': short_url}), 201


@app.route('/<short_url>', methods=['GET'])
def redirect_to_original_url(short_url):
    """ Accepts a GET to the root endpoint, with a short_url path parameter, e.g.
    curl -i localhost:8080/BdhHbLINOA,
    :return if the short url is found, redirects to its original url, if not, a 404 (not found) is returned """

    try:
        original_url = SHORT_URL_CONTROLLER.get_original_url(short_url)
    except:
        return "Not found", 404
    if original_url:
        url = original_url.url
        if not original_url.url.startswith("http"):
            url = "http://" + url
        return redirect(url), 307
    else:
        return "Not found", 404
