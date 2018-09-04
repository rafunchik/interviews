package rcastro.wikiassistant.domain

import rcastro.wikiassistant.domain.model.{Article, SQLResultContainer}

trait SQLStatementRepository {

  def runStatement(statement: String): Either[Throwable, SQLResultContainer]

  def mostOutdatedArticleInCategory(category: String): Either[Throwable, SQLResultContainer]

}
