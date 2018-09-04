package rcastro.wikiassistant.framework.adapter

import cats.implicits._
import cats.syntax.either._
import rcastro.wikiassistant.domain.SQLStatementRepository
import rcastro.wikiassistant.domain.model.Article


case class TimedResult(result: String, time: String)

case class SQLErrorGettingPage(cause: Throwable) extends Throwable

case class SQLStatementAdapter(repository: SQLStatementRepository) {

  def mostOutdatedArticleInCategory(category: String): Either[Throwable, TimedResult] = {
    val t0 = System.nanoTime()
    repository.mostOutdatedArticleInCategory(category).map { results => //FIXME use DTO and wrapping trait for timed operations
      val t1 = System.nanoTime()
      TimedResult(results.result, (t1 - t0).toString)
    }.leftMap(SQLErrorGettingPage)
  }

  def runStatement(sqlStatement: String): Either[Throwable, TimedResult] = {
    val t0 = System.nanoTime()
    repository.runStatement(sqlStatement).map { results =>
      val t1 = System.nanoTime()
      TimedResult(results.result, (t1 - t0).toString)
    }.leftMap(SQLErrorGettingPage)
  }
}
