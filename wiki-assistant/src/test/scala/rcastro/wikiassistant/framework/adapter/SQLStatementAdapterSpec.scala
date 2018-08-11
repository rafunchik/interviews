package rcastro.wikiassistant.framework.adapter

import org.specs2.mock.Mockito
import org.specs2.mutable.Specification
import rcastro.wikiassistant.domain.SQLStatementRepository
import rcastro.wikiassistant.domain.model.{Article, SQLResultContainer}


class SQLStatementAdapterSpec extends Specification with Mockito {

  "SQLStatementAdapterSpec" should {
    "mostOutdatedArticleInCategory" in {
      val mockRepo = mock[SQLStatementRepository]
      val category = "fruit"
      val outdatedArticle = Some(Article("orange", "1 day"))
      mockRepo.mostOutdatedArticleInCategory(category) returns outdatedArticle
      val adapter = SQLStatementAdapter(mockRepo)

      val result = adapter.mostOutdatedArticleInCategory(category)

      result must beEqualTo(Right(outdatedArticle))
    }

    "runStatement" in {
      val mockRepo = mock[SQLStatementRepository]
      val statement = "select * from page;"
      val resultString = "1|orange|2003-02-01 00:00:00|"
      mockRepo.runStatement(statement) returns SQLResultContainer(resultString)
      val adapter = SQLStatementAdapter(mockRepo)

      val expected = adapter.runStatement(statement).right.get
      val expectedResult = expected.result
      val expectedExecutionTime = expected.time.toLong

      expectedResult must beEqualTo(resultString)
      expectedExecutionTime must beGreaterThan(0L)
    }

    //TODO negative scenarios
  }
}
