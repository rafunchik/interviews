
*Url shortener*

Your primary task is to build a URL shortener web service using Java, Scala or Python.

*Requirements*

Your web service should have a POST /shorten_url endpoint that receives a JSON body with the URL to shorten. 
A successful request will return a JSON body with the shortened url. If a GET request is made to the shortened URL then 
the user should be redirected to the the original URL, or returned the contents of the original URL. It should perform 
appropriate validation on the URL to be shortened, and return appropriate error responses if the URL is not valid. It 
should contain a README.md file with instructions on how to run your service.


Assumptions:

- Urls are randomly generated by the service, and returned prepended with the service name (http://www.your_service.com/)
- If a GET request is made to the shortened URL then the user will be redirected to the original URL
- The short urls can have a TTL
- Dealing with a maximum of a billion active urls at the same time
- A valid url is what `Uri.uri` can parse (same as `java.net.URI`)
- Using http4s as the minimalistic functional Scala web framework and Flask for the Python version


Run:

- `sbt run`
- `curl -H "Content-Type: application/json" -d '{"url": "www.hello.com"}' http://localhost:8080/shorten_url`
- `curl -i localhost:8080/BdhHbLINOA`
- to run the tests, `sbt test`
- for the Python version, `make run` inside python_url_shortener/short_url, or run `pytest` to run the tests


Use cases:

- Shortening a URL to a Short Url.
- Redirecting to the URL associated with a Short Url.


Notes:

- If some links are accessed much more often than others, use cache with expiry for most frequently accessed urls 
  (LRU, Map + LinkedHashMap) 
- Once deployed to, let's say AWS, should use an ELB to distribute the load horizontally among the machines
- Short url combinations, make 36^10 combinations, collisions are highly unlikely
- The app should scale using the inmemory repository, if this were not enough due to memory constraints, can use a 
  distributed sharded repository: hash key based for instance, (we have a set maximum of urls), another possibility is 
  using a lookup table for the partitioned data, but then that table would become a single point of failure. 
- We would have have janitor job to remove outdated urls or use ttl directly like in redis, when putting the urls.
- if it were an expensive process to generate url (e.g. dns etc), or storing it, would need to do it asynchronously, 
  request gets into queue, then gets processed by another job, and the user gets optionally notified upon completion.
- If we store the page content too, this could go into a separate repository and join data in the controller when 
  requested (can also add a page summary to the original url object in memory). 
- TODO, use `java.net.URI` instead of `http4s` `Uri` to decrease coupling to the framework (using as it is Scala, 
  more convenient)
- The tests could do with some additional cleaning






