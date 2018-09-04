package rcastro.wikiassistant.framework

import java.net.URLDecoder

import cats.effect.{IO, _}
import org.http4s.headers._
import org.http4s.server._
import org.http4s.dsl.Http4sDsl
import org.http4s.{HttpService, Request, Response, UrlForm}
import cats.implicits._
import rcastro.wikiassistant.domain.model.Article
import rcastro.wikiassistant.framework.adapter.{SQLStatementAdapter, TimedResult}
import rcastro.wikiassistant.framework.repository.MySQLStatementRepository
import org.http4s.headers.`Content-Type`
import org.http4s.MediaType.`text/html`
import org.http4s._
import org.http4s.MediaType
import org.http4s.circe._
import org.http4s._
import org.http4s.dsl.Http4sDsl
import org.http4s.multipart.{Multipart, Part}
import org.http4s.server.blaze.BlazeBuilder
import org.http4s.MediaType._
import org.http4s.headers._

import scala.util.Try



class WikiService[IO[_]: Effect] extends Http4sDsl[IO] {

  private val adapter = SQLStatementAdapter(new MySQLStatementRepository())

  val service: HttpService[IO] = defineService(adapter)


  def defineService(adapter: SQLStatementAdapter): HttpService[IO] = {
    HttpService[IO] {
      case GET -> Root =>
        Ok("""<h2>App options</h2>
      <ul>
        <li><a href=most-outdated>Find the most outdated page</a></li>
        <li><a href=sql>Run a SQL query</a></li>
      </ul>""", `Content-Type`(`text/html`)) //TODO extract into html templates and use Twirl perhaps

      case GET -> Root / "most-outdated" =>
        Ok("""<html>
          <body>
            <form name="input" method="post">
              <p>category: <input type="text" name="category"/></p>
              <p><input type="submit" value="Submit"/></p>
            </form>
          </body>
        </html>""", `Content-Type`(`text/html`))

      case req @ POST -> Root / "most-outdated" =>
        req.decode[String] { data =>
          decodeForm(data) //FIXME implement proper UrlForm decoder
            .map(category => mostOutdatedPageInCategory(adapter, category))
            .getOrElse(BadRequest("Category missing"))
        }

      case GET -> Root / "sql" =>
        Ok("""<html>
          <body>
            <form name="input" method="post">
              <p>query: <input type="text" name="query" style="width: 506px;height: 31px;"/></p>
              <p><input type="submit" value="Submit"/></p>
            </form>
          </body>
        </html>""", `Content-Type`(`text/html`))

      case req @ POST -> Root / "sql" =>
        //TODO validation
        req.as[String].flatMap { data =>
          decodeForm(data) //FIXME implement proper UrlForm decoder
            .map(sqlStatement => runSQLStatement(adapter, sqlStatement))
            .getOrElse(BadRequest("SQL query missing"))
        }
    }
  }

  private def decodeForm(data: String) = {
    Try(URLDecoder.decode(data.split("=")(1), "utf-8"))
  }

  private def runSQLStatement(adapter: SQLStatementAdapter, sqlStatement: String) = {
    adapter.runStatement(sqlStatement.replaceAll("(?i)ALTER TABLE", "")) match { //FIXME implement proper validation
      case Right(result) => createSQLResponse(result)
      case Left(error) => InternalServerError(s"${error}")
    }
  }

  private def mostOutdatedPageInCategory(adapter: SQLStatementAdapter, category: String) = {
    println(category)
    adapter.mostOutdatedArticleInCategory(category) match {
      case Right(result) => createArticleResponse(result)
      case Left(error) => InternalServerError(s"${error.getLocalizedMessage}")
    }
  }

  private def createSQLResponse(result: TimedResult): IO[Response[IO]] = {
    Ok(s"""
       <div>${result.result}</div>
       <br><br>
       <div>Execution time: ${result.time}</div>
       <br><br>
       <a href=sql>Run another SQL query</a>""", `Content-Type`(`text/html`))
  }

  private def createArticleResponse(result: TimedResult) = {
      Ok(s"""
        <div>${result.result}</div>
        <br><br>
        <div>Execution time ${result.time}ns</div>
        <br><br>
        <a href=\"most-outdated\" class="btn btn-info">Find the most outdated page</a>""", `Content-Type`(`text/html`))
  }

}
