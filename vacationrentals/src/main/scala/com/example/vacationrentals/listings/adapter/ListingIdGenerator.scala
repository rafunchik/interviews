package com.example.vacationrentals.listings.adapter

import java.util.UUID.randomUUID

case class IdGenerationError(throwable: Throwable)

trait ListingIdGenerator {

  def generate(newListingDTO: ListingDTO): String

}

object ListingIdGenerator extends ListingIdGenerator {
  def generate(newListingDTO: ListingDTO): String = randomUUID.toString
}
