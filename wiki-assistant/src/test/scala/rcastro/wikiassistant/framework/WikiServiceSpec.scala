package rcastro.wikiassistant.framework

import cats.effect.IO
import cats.implicits._
import org.http4s.circe._
import org.http4s.dsl.io._
import org.http4s.{Uri, _}
import org.specs2.mock.Mockito
import org.specs2.mutable.Specification

class WikiServiceSpec extends Specification {
  "WikiService" >> {
    //TODO use mock adapter
    "should return 200 when querying for the most outdated page in a category" >> {
      val request = Request[IO](method = Method.GET, uri = Uri.uri("/most-outdated/fruit"))
      val response = new WikiService[IO].service.orNotFound(request).unsafeRunSync()
      response.status must beEqualTo(Status.Ok)
    }

    "should run a sql statement returning its result and timing" >> {
      val request = Request[IO](method = Method.POST, uri = Uri.uri("/sql")).withBody("select * from page;").unsafeRunSync()
      val response = new WikiService[IO].service.orNotFound(request).unsafeRunSync()
      response.status must beEqualTo(Status.Ok)
    }

    //TODO negative/invalid cases
  }
}
