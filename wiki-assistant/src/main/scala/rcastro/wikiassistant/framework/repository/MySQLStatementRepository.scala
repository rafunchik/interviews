package rcastro.wikiassistant.framework.repository

import java.sql.{PreparedStatement, ResultSet}

import cats.effect.IO
import doobie._
import doobie.implicits._
import rcastro.wikiassistant.domain.SQLStatementRepository
import rcastro.wikiassistant.domain.model.{Article, SQLResultContainer}

import scala.slick.driver.MySQLDriver
import scala.slick.driver.MySQLDriver.simple._
import cats.implicits._

case class ModifiedArticle(id: Int, title: String, modified: String)

class MySQLStatementRepository() extends SQLStatementRepository {

//  lazy val XA = Transactor.fromDriverManager[IO](
//    "org.mysql.Driver", "jdbc:mysql:wikis"
//  )

  override def runStatement(statement: String): Either[Throwable, SQLResultContainer] = {
    //TODO use doobie
    Either.catchNonFatal {
      Database.forConfig("mysql") withSession {
        implicit session: MySQLDriver.backend.Session =>

          val preparedStatement: PreparedStatement = session.prepareStatement(statement)
          val results: ResultSet = preparedStatement.executeQuery()
          var resultStr = ""
          while (results.next) {
            val columnsNumber = results.getMetaData.getColumnCount
            for(i <- 1 to columnsNumber) {
              resultStr += results.getString(i) + "|"
            }
            resultStr += "\n"
          }
          SQLResultContainer(resultStr)
      }
    }
  }

  override def mostOutdatedArticleInCategory(category: String): Either[Throwable, SQLResultContainer] = {
//
//    val statement =
//      sql"""select page_title, max_modified
//           |from (
//           |select p.page_id, p.page_title from wikipage p join categorylinks cl on p.page_id=cl.cl_from
//           |where cl.cl_to = $category
//           |) as categorized inner join (select p.page_id, max(ap.rev_timestamp - p.rev_timestamp) as max_modified
//           |from wikipage p join pagelinks l on p.page_id=l.pl_from join wikipage ap on l.pl_title=ap.page_title
//           |group by p.page_id) as modified
//           |on categorized.page_id = modified.page_id order by max_modified desc limit 1;"""

    val result = runStatement(
      s"""select page_title
         |from ( select p.page_id, p.page_title from wikipage p join categorylinks cl
         |on p.page_id=cl.cl_from where cl.cl_to = '$category' ) as categorized inner join
         |(select p.page_id, max(ap.rev_timestamp - p.rev_timestamp) as max_modified from wikipage p join pagelinks l
         |on p.page_id=l.pl_from join wikipage ap on l.pl_title=ap.page_title group by p.page_id) as modified on
         |categorized.page_id = modified.page_id order by max_modified desc limit 1;""".stripMargin)
    result
//    val result = statement.query[ModifiedArticle].option.transact(XA).unsafeRunSync
//    result.map(modifiedArticle =>
//      Article(modifiedArticle.title, modifiedArticle.modified.toString))
  }
}

