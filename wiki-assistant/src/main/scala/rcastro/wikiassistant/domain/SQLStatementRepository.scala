package rcastro.wikiassistant.domain

import java.sql.ResultSet

import rcastro.wikiassistant.domain.model.{Article, SQLResultContainer}

trait SQLStatementRepository {
  def runStatement(statement: String): SQLResultContainer

  def mostOutdatedArticleInCategory(category: String): Option[Article]

}
