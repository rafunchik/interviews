package com.example.vacationrentals.listings.restservice

import cats.effect.Effect
import cats.implicits._
import com.example.vacationrentals.listings.adapter.{ListingDTO, ListingIdGenerator, ListingsAdapter, SavedListingDTO}
import com.example.vacationrentals.listings.repository.ListingsInMemoryRepository
import com.example.vacationrentals.listings.restservice.entities.{Address, Contact, Location}
import io.circe.generic.auto._
import io.circe.syntax._
import org.http4s.HttpService
import org.http4s.circe.jsonEncoder
import org.http4s.dsl.Http4sDsl

import scala.util.Try

case class CreatedListingResponse(id: String)
case class UpdatedListingResponse(id: String)


class ListingService[F[_]: Effect] extends Http4sDsl[F] {

  private implicit val repo = ListingsInMemoryRepository()
  private implicit val idGenerator = ListingIdGenerator

  private val listingsAdapter = ListingsAdapter()

  private val Listings = "listings"

  val service: HttpService[F] = defineService(listingsAdapter)

  def defineService(listingsAdapter: ListingsAdapter): HttpService[F] = {
    HttpService[F] {

      case GET -> Root / Listings / listingId =>

        listingsAdapter.get(listingId) match {
          case Some(listingDTO)  => Ok(savedListingDTOToListingResponse(listingDTO).asJson)
          case _                 => NotFound("Listing not found")
        }

      case request @POST -> Root / Listings =>
        import org.http4s.circe.CirceEntityDecoder._

        Try(
          request.as[UpdateListingRequest].attempt.flatMap {
            case Right(listing) => create(listingsAdapter, listing)
            case Left(_)        => BadRequest("Error decoding the request")
          }
        ).getOrElse(InternalServerError("Error creating listing"))

      case request @PUT -> Root / Listings / listingId =>
        import org.http4s.circe.CirceEntityDecoder._

        Try(
          request.as[UpdateListingRequest].attempt.flatMap {
            case Right(listing) => update(listingsAdapter, listing, listingId)
            case Left(_)        => BadRequest("Error decoding the request")
          }
        ).getOrElse(InternalServerError("Error updating listing"))

      case DELETE -> Root / Listings / listingId =>

        listingsAdapter.delete(listingId) match {
          case Some(removedId)  => Ok(s"Listing $removedId removed")
          case _                => NotFound("Listing not found")
        }
    }
  }


  private def update(listingsAdapter: ListingsAdapter, listing: UpdateListingRequest, listingId: String) = {
    listingsAdapter.update(updateRequestToSavedListingDTO(listing, listingId)) match {
      case Some(_) => Ok(UpdatedListingResponse(listingId).asJson)
      case _       => Created(CreatedListingResponse(listingId).asJson)
    }
  }

  private def create(listingsAdapter: ListingsAdapter, listingRequest: UpdateListingRequest) = {
    listingsAdapter.put(createRequestToListingDTO(listingRequest)) match {
      case Right(createdListingId) => Created(CreatedListingResponse(createdListingId).asJson)
      case Left(_)                 => InternalServerError("Error generating a listing ID")
    }
  }

  private def savedListingDTOToListingResponse(savedListingDTO: SavedListingDTO) = {
    val dto = savedListingDTO.listingDTO
    val listing = ListingRepresentation(
      id = savedListingDTO.id,
      contact = Contact(
        phone = dto.phone,
        formattedPhone = dto.formattedPhone),
      address = Address(
        address = dto.address,
        postalCode = dto.postalCode,
        countryCode = dto.countryCode,
        city = dto.city,
        state = dto.state,
        country = dto.country),
      location = Location(dto.lat, dto.lng)
    )
    ListingResponse(listing)
  }

  private def requestPartsToListingDTO(contact: Contact, address: Address, location: Location): ListingDTO = {
    ListingDTO(
      phone = contact.phone,
      formattedPhone = contact.formattedPhone,
      address = address.address,
      postalCode = address.postalCode,
      countryCode = address.countryCode,
      city = address.city,
      state = address.state,
      country = address.country,
      lat = location.lat,
      lng = location.lng)
  }

  private def updateRequestToSavedListingDTO(listingRequest: UpdateListingRequest, listingId: String): SavedListingDTO = {
    SavedListingDTO(
      listingId,
      requestPartsToListingDTO(listingRequest.contact, listingRequest.address, listingRequest.location))
  }

  private def createRequestToListingDTO(listingRequest: UpdateListingRequest): ListingDTO = {
    requestPartsToListingDTO(listingRequest.contact, listingRequest.address, listingRequest.location)
  }
}
