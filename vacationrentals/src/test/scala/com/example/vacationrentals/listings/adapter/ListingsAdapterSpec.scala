package com.example.vacationrentals.listings.adapter

import com.example.vacationrentals.listings.domain.Listing
import com.example.vacationrentals.listings.repository.ListingsInMemoryRepository
import org.specs2.mock.Mockito
import org.specs2.mutable.Specification
import org.mockito.ArgumentMatchers.{eq => mockitoEq}


class ListingsAdapterSpec extends Specification with Mockito {
  import ListingsAdapterSpec._

  "ListingsAdapter" should {

    "put should try generating an ID for a limited amount of time, and then timeout with an error" in {
      implicit val mockedRepo = mock[ListingsInMemoryRepository]
      implicit val mockedIdGenerator = mock[ListingIdGenerator]
      mockedIdGenerator.generate(any()) returns "someid"
      for (i <- 1 to 10) {
        mockedRepo.putIfabsent(any(), any()) returns Some(TestListing)
      }
      val adapter = ListingsAdapter()

      val result = adapter.put(TestListingDTO)

      result must beLeft
    }

    "put should try generating a new ID, upon a collision" in {
      val id2 = "xcrw222"
      implicit val mockedRepo = mock[ListingsInMemoryRepository]
      mockedRepo.putIfabsent(mockitoEq(ListingID), any()) returns Some(TestListing)
      mockedRepo.putIfabsent(mockitoEq(id2), any()) returns None
      implicit val mockedUrlGenerator = mock[ListingIdGenerator]
      mockedUrlGenerator.generate(any()) returns ListingID thenReturns id2
      val adapter = ListingsAdapter()

      val result = adapter.put(TestListingDTO)

      result must beRight[String]
    }
  }
}

object ListingsAdapterSpec {

  val TestListing = Listing(
    id = "anId",
    phone = "15126841100",
    formattedPhone = "+1 512-684-1100",
    address = "1011 W 5th St",
    postalCode = Some("1011"),
    countryCode = "US",
    city = "Austin",
    state = Some("TX"),
    country = "United States",
    lat = 40.4255485534668,
    lng = -3.7075681686401367
  )

  val TestListingDTO = ListingDTO(
    phone = "15126841100",
    formattedPhone = "+1 512-684-1100",
    address = "1011 W 5th St",
    postalCode = Some("1011"),
    countryCode = "US",
    city = "Austin",
    state = Some("TX"),
    country = "United States",
    lat = 40.4255485534668,
    lng = -3.7075681686401367
  )

  val ListingID = "anId"

}
