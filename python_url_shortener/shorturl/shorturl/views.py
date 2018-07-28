from flask import render_template, request, abort, redirect, url_for

from shorturl import app


@app.route('/shorten_url', methods=['HEAD, POST'])
def shorten_url():
    """ Accepts a POST to the shorten_url endpoint, with a valid JSON url object, e.g.
    curl -H "Content-Type: application/json" -d '{"url": "www.hello.com"}' http://localhost:8080/shorten_url
    generates, saves and returns a new shortened url """

    if request.method == 'POST':
        app.logger.warning('sample message')
        return render_template('index.html')


@app.route('/<short_url>', methods=['GET'])
def redirect_to_original_url():
    app.logger.warning('sample message')
    return redirect("")  # url_for('login'))


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