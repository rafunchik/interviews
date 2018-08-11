package rcastro.wikiassistant.framework.repository

import java.sql.{PreparedStatement, ResultSet}

import cats.effect.IO
import doobie._
import doobie.implicits._
import rcastro.wikiassistant.domain.SQLStatementRepository
import rcastro.wikiassistant.domain.model.{Article, SQLResultContainer}

import scala.slick.driver.PostgresDriver
import scala.slick.driver.PostgresDriver.simple._

case class ModifiedArticle(id: Int, title: String, modified: String)

class PostgresSQLStatementRepository(connectionUrl: String = "jdbc:postgresql://localhost/wikis") extends SQLStatementRepository {

  lazy val XA = Transactor.fromDriverManager[IO](
    "org.postgresql.Driver", "jdbc:postgresql:wikis"
  )

  override def runStatement(statement: String): SQLResultContainer = {
    //TODO use doobie and then mostOutdatedArticleInCategory should call this one

    Database.forURL(connectionUrl, driver = "org.postgresql.Driver") withSession {
      implicit session: PostgresDriver.backend.Session =>

        val preparedStatement: PreparedStatement = session.prepareStatement(statement)
        val results: ResultSet = preparedStatement.executeQuery()
        var resultStr = ""
        while (results.next) {
          println(results)
          val columnsNumber = results.getMetaData.getColumnCount
          for(i <- 1 to columnsNumber) {
            resultStr += results.getString(i) + "|"
          }
          resultStr += "\n"
        }
        SQLResultContainer(resultStr)
    }
  }

  override def mostOutdatedArticleInCategory(category: String): Option[Article] = {


    val statement =
      sql"""select *
      from (
      select p.page_id, p.title from page p join category_page cp on p.page_id=cp.page_id
      join category c on cp.category_id=c.category_id where c.title = $category
      ) as categorized inner join (select p.page_id, max(ap.modified - p.modified) as max_modified
      from page p join links l on p.page_id=l.page_id join page ap on l.linked_page_id=ap.page_id group by p.page_id) as modified
      on categorized.page_id = modified.page_id;"""


    val result = statement.query[ModifiedArticle].option.transact(XA).unsafeRunSync

    result.map(modifiedArticle =>
      Article(modifiedArticle.title, modifiedArticle.modified.toString))
  }

}
