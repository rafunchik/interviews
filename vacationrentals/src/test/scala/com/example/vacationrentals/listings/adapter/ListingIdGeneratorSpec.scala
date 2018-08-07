package com.example.vacationrentals.listings.adapter

import org.specs2.mutable.Specification

class ListingIdGeneratorSpec extends Specification {

  "ListingIdGenerator" should {
    "generate a different String every time" in {
      val someListingDTO = ListingDTO("", "", "", None, "","", None,"",0, 0)

      val generated = Set(
        ListingIdGenerator.generate(someListingDTO),
        ListingIdGenerator.generate(someListingDTO),
        ListingIdGenerator.generate(someListingDTO))

      generated.size must beEqualTo(3)
      forall(generated) {
        id => {
          id.length must beGreaterThan(10)
        }
      }
    }

  }
}
