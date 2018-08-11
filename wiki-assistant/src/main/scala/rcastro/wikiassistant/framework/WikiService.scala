package rcastro.wikiassistant.framework

import cats.effect.{IO, _}
import org.http4s.dsl.Http4sDsl
import org.http4s.{HttpService, Request, Response}
import cats.implicits._
import rcastro.wikiassistant.domain.model.Article
import rcastro.wikiassistant.framework.adapter.{SQLStatementAdapter, TimedResult}
import rcastro.wikiassistant.framework.repository.PostgresSQLStatementRepository



class WikiService[IO[_]: Effect] extends Http4sDsl[IO] {

  private val adapter = SQLStatementAdapter(new PostgresSQLStatementRepository())

  val service: HttpService[IO] = defineService(adapter)


  def defineService(adapter: SQLStatementAdapter): HttpService[IO] = {
    HttpService[IO] {
      case GET -> Root / "most-outdated" / category =>
        adapter.mostOutdatedArticleInCategory(category) match {
          case Right(result) => createArticleResponse(result)
          case Left(error)   => InternalServerError(s"${error.getLocalizedMessage}")
        }

      case req @ POST -> Root / "sql" =>
        req.as[String].flatMap { sqlStatement =>
          adapter.runStatement(sqlStatement) match {
            case Right(result) => createSQLResponse(result)
            case Left(error) => InternalServerError(s"${error.getLocalizedMessage}")
          }
        }
    }
  }

  private def createSQLResponse(result: TimedResult): IO[Response[IO]] = {
    Ok(s"result and execution time ${result.result}, ${result.time}") //TODO return html
  }

  private def createArticleResponse(result: Option[Article]) = {
    result match {
      case Some(article) => Ok(s"the most outdated article is ${article.title}, since ${article.lastModified}") //TODO return html
      case None          => NotFound("there was no outdated article for the given category")
    }
  }

  private def extractSql(request: Request[IO]) = {

        request.as[String].attempt

  } //TODO validation
}
