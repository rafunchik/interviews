package com.example.vacationrentals.listings.adapter

import cats.implicits._
import com.example.vacationrentals.listings.domain.{Listing, ListingsRepository}

import scala.util.control.Breaks._


case class ListingDTO(phone: String,
                      formattedPhone: String,
                      address: String,
                      postalCode: Option[String],
                      countryCode: String,
                      city: String,
                      state: Option[String],
                      country: String,
                      lat: Double,
                      lng: Double)

case class SavedListingDTO(id: String, listingDTO: ListingDTO)

case class IdGenerationTimeoutException(message: String) extends Exception

case class ListingsAdapter(implicit listingsRepository: ListingsRepository,
                           listingIdGenerator: ListingIdGenerator) {

  def get(listingId: String): Option[SavedListingDTO] = {
    listingsRepository
      .get(listingId)
      .map(listingToSavedListingDTO)
  }

  def delete(listingId: String): Option[String] = {
    listingsRepository
      .delete(listingId)
      .map(listing => listing.id)
  }

  def update(savedListingDTO: SavedListingDTO): Option[SavedListingDTO] = {
    val listing = savedListingDTOToListing(savedListingDTO)
    listingsRepository
      .put(listing.id, listing)
      .map(listingToSavedListingDTO)
  }

  def put(newListingDTO: ListingDTO): Either[Throwable, String] = {
    val (listingId: String, couldPut: Boolean) = tryToGenerateIdAndPut(newListingDTO)

    if (couldPut){
      listingId.asRight
    }
    else {
      IdGenerationTimeoutException(s"Timed out generating a new ID for the listing").asLeft
    }
  }

  private def tryToGenerateIdAndPut(newListingDTO: ListingDTO): (String, Boolean) = {
    var listingId = listingIdGenerator.generate(newListingDTO)
    var couldPut = false
    //TODO make real timeout
    breakable {
      for (i <- 1 to 10) {
        val dto = SavedListingDTO(listingId, newListingDTO)
        val listing = savedListingDTOToListing(dto)
        listingsRepository.putIfabsent(listingId, listing) match {
          case Some(_) =>
            listingId = listingIdGenerator.generate(newListingDTO)
          case None    =>
            couldPut = true
            break
        }
      }
    }
    (listingId, couldPut)
  }

  private def savedListingDTOToListing: SavedListingDTO => Listing = {
    savedListingDTO =>
      Listing(
        id = savedListingDTO.id,
        phone = savedListingDTO.listingDTO.phone,
        formattedPhone = savedListingDTO.listingDTO.formattedPhone,
        address = savedListingDTO.listingDTO.address,
        postalCode = savedListingDTO.listingDTO.postalCode,
        countryCode = savedListingDTO.listingDTO.countryCode,
        city = savedListingDTO.listingDTO.city,
        state = savedListingDTO.listingDTO.state,
        country = savedListingDTO.listingDTO.country,
        lat = savedListingDTO.listingDTO.lat,
        lng = savedListingDTO.listingDTO.lng)
  }

  private def listingToListingDTO: Listing => ListingDTO = {
    listing =>
      ListingDTO(
        phone = listing.phone,
        formattedPhone = listing.formattedPhone,
        address = listing.address,
        postalCode = listing.postalCode,
        countryCode = listing.countryCode,
        city = listing.city,
        state = listing.state,
        country = listing.country,
        lat = listing.lat,
        lng = listing.lng)
  }

  private def listingToSavedListingDTO: Listing => SavedListingDTO = {
    listing =>
      SavedListingDTO(
        id = listing.id,
        listingDTO = listingToListingDTO(listing))
  }

}
