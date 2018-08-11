package rcastro.wikiassistant.framework

import cats.effect._
import cats.implicits._
import rcastro.wikiassistant.domain.SQLStatementRepository
import rcastro.wikiassistant.domain.model.Article


case class TimedResult(result: String, time: String)

case class SQLErrorGettingPage(cause: Throwable) extends Throwable

case class SQLStatementAdapter(repository: SQLStatementRepository) {

  def mostOutdatedArticleInCategory(category: String): Either[Throwable, Option[Article]] = {
    Either.catchNonFatal {
      repository.mostOutdatedArticleInCategory(category) //FIXME use DTO
    }.leftMap(SQLErrorGettingPage)
  }

  def runStatement(sqlStatement: String): Either[Throwable, TimedResult] = {
      println(s"statement: $sqlStatement")

      val t0 = System.nanoTime()
      val results = repository.runStatement(sqlStatement)
      val t1 = System.nanoTime()
      println(results.result)
      println("Elapsed time: " + (t1 - t0) + "ns")

      TimedResult(results.result, (t1 - t0).toString).asRight
  }

}
