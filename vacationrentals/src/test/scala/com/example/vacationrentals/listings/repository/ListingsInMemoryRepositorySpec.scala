package com.example.vacationrentals.listings.repository

import com.example.vacationrentals.listings.domain.Listing
import org.specs2.mutable.Specification

class ListingsInMemoryRepositorySpec extends Specification {
  import ListingsInMemoryRepositorySpec._

  "ListingsInMemoryRepository" should {

    "be able to update a listing" in {
      val repo = ListingsInMemoryRepository()

      repo.put(ListingID, EarlierListing)
      repo.put(ListingID, TestListing)

      repo.get(ListingID) must beSome(TestListing)
    }

    "get a None if the listing is not present" in {
      val repo = ListingsInMemoryRepository()
      val id = "notFoundId"

      repo.get(id) must beNone
    }

    "put and get the same id - listing pair" in {
      val repo = ListingsInMemoryRepository()

      repo.put(ListingID, TestListing)

      repo.get(ListingID) must beSome(TestListing)
    }

    "putIfAbsent should not update if present" in {
      val repo = ListingsInMemoryRepository()

      repo.put(ListingID, EarlierListing)
      repo.putIfabsent(ListingID, TestListing)

      repo.get(ListingID) must beSome(EarlierListing)
    }

    "putIfAbsent should update if not present" in {
      val repo = ListingsInMemoryRepository()

      repo.putIfabsent(ListingID, TestListing)

      repo.get(ListingID) must beSome(TestListing)
    }

    "delete should delete if present" in {
      val repo = ListingsInMemoryRepository()

      repo.put(ListingID, TestListing)
      repo.delete(ListingID)

      repo.get(ListingID) must beNone
    }
  }
}

object ListingsInMemoryRepositorySpec {

  val TestListing = Listing(
    id = "123-123",
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
  val EarlierListing: Listing = TestListing.copy(phone = "11")

}