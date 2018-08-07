package com.example.vacationrentals.listings.restservice

import cats.effect.IO
import com.example.vacationrentals.listings.adapter.{ListingIdGenerator, ListingsAdapter}
import com.example.vacationrentals.listings.domain.Listing
import com.example.vacationrentals.listings.repository.ListingsInMemoryRepository
import com.example.vacationrentals.listings.restservice.entities.{Address, Contact, Location}
import io.circe.Json
import io.circe.generic.auto._
import io.circe.syntax._
import io.circe.literal._
import org.http4s.circe.{jsonOf, _}
import org.http4s.dsl.io._
import org.http4s.{Uri, _}
import org.mockito.ArgumentMatchers.{eq => mockitoEq}
import org.specs2.mock.Mockito




class ListingServiceSpec extends org.specs2.mutable.Specification with Mockito {
  import ListingServiceSpec._

  implicit val decoder = jsonOf[IO, CreatedListingResponse]
  implicit val decoder2 = jsonOf[IO, UpdateListingRequest]
  implicit val decoder3 = jsonOf[IO, ListingResponse]


  "Listings service: " >> {

    "should be able to create a valid listing and return it successfully" >> {
      val listingService = new ListingService[IO]
      val postResponse: Response[IO] = createValidListingResponse(listingService)
      val id = postResponse.as[CreatedListingResponse].unsafeRunSync().id
      val expectedListing = ExpectedListing.copy(id = id)

      val getRequest = Request[IO](method = Method.GET, uri = Uri.fromString(s"/listings/$id").right.get)

      val response = listingService.service.orNotFound(getRequest).unsafeRunSync()
      response.status must beEqualTo(Status.Ok)
      response.as[ListingResponse].unsafeRunSync() must beEqualTo(ListingResponse(listing = expectedListing))
    }

    "should return 400 when trying to add a new listing with a malformed JSON body" >> {
      val request = Request[IO](method = Method.POST, uri = Uri.uri("/listings"))
        .withBody(MalformedJSON)
        .unsafeRunSync()

      checkStatus(request, Status.BadRequest)
    }

    "should return 404 when trying to get a not found url" >> {
      val request = Request[IO](Method.GET, Uri.uri("/unknown_short_url"))

      checkStatus(request, Status.NotFound)
    }

    "should return 404 when trying to get a not found listing" >> {
      val request = Request[IO](Method.GET, Uri.uri("/listings/not_found_id"))

      checkStatus(request, Status.NotFound)
    }

    "should return 500 upon an error generating an ID when creating a new listing" >> {
      val request = Request[IO](Method.POST, Uri.uri("/listings"))
        .withBody(ValidJsonRequest)
        .unsafeRunSync()
      implicit val mockRepo: ListingsInMemoryRepository = mock[ListingsInMemoryRepository]
      implicit val idGenerator: ListingIdGenerator.type = ListingIdGenerator
      val adapter = ListingsAdapter()
      mockRepo.putIfabsent(any(), any()) returns Some(SomeListing)

      val response = new ListingService[IO].defineService(adapter).orNotFound(request).unsafeRunSync()

      response.status must beEqualTo(Status.InternalServerError)
    }

    "should be able to create a new listing from a valid listing json document" >> {
      val listingService = new ListingService[IO]
      val postResponse: Response[IO] = createValidListingResponse(listingService)

      postResponse.status must beEqualTo(Status.Created)
    }

    "should be able to create a new listing from a valid listing json document with the optional fields missing" >> {
      val listingService = new ListingService[IO]
      val postResponse: Response[IO] = createValidListingResponse(listingService, ValidOptionalJsonRequest)

      postResponse.status must beEqualTo(Status.Created)
    }

    "should not be able to create a new listing from an invalid listing json document" >> {
      val listingService = new ListingService[IO]
      val postResponse: Response[IO] = createValidListingResponse(listingService, WrongCountryCodeJSON)

      postResponse.status must beEqualTo(Status.BadRequest)
    }

    "should return 404 when trying to delete a not found listing" >> {
      val request = Request[IO](Method.DELETE, Uri.uri("/listings/not_found_id"))

      checkStatus(request, Status.NotFound)
    }

    "should be able to create a valid listing and delete it successfully " >> {
      val listingService = new ListingService[IO]
      val postResponse: Response[IO] = createValidListingResponse(listingService)

      val id = postResponse.as[CreatedListingResponse].unsafeRunSync().id

      val getRequest = Request[IO](method = Method.DELETE, uri = Uri.fromString(s"/listings/$id").right.get)

      val response = listingService.service.orNotFound(getRequest).unsafeRunSync()
      response.status must beEqualTo(Status.Ok)
    }
  }

  private def createValidListingResponse(listingService: ListingService[IO], responseBody: Json = ValidJsonRequest) = {
    val postRequest = Request[IO](method = Method.POST, uri = Uri.uri("/listings"))
      .withBody(responseBody)
      .unsafeRunSync()
    val postResponse = listingService.service.orNotFound(postRequest).unsafeRunSync()
    postResponse
  }

  private def checkStatus(request: Request[IO], status: Status) = {
    val response = new ListingService[IO].service.orNotFound(request).unsafeRunSync()
    response.status must beEqualTo(status)
  }
}

object ListingServiceSpec {
  private val contact = Contact(
    phone = "15126841100",
    formattedPhone = "+1 512-684-1100"
  )
  private val address = Address(
    address = "1011 W 5th St",
    postalCode = Some("1011"),
    countryCode = "US",
    city = "Austin",
    state = Some("TX"),
    country = "United States"
  )
  private val location = Location(
    lat = 40.4255485534668,
    lng = -3.7075681686401367
  )

  private val ExpectedListing = ListingRepresentation("", contact, address, location)
  private val SomeListing = Listing("", "", "", "",None, "","", None,"",0 ,0)

  private val ValidJsonRequest = UpdateListingRequest(
    contact = contact,
    address = address,
    location = location).asJson

  private val ValidOptionalJsonRequest: Json = UpdateListingRequest(
    contact = contact,
    address = address.copy(postalCode = None, state = None),
    location = location).asJson

  private val MalformedJSON = "\"city\": \"LA\"}}}}"

  private val WrongCountryCodeJSON =
    json"""{
      "listing": {
        "id": "5e22a83a-6f4f-11e6-8b77-86f30ca893d3",
        "contact": {
        "phone": "15126841100",
        "formattedPhone": "+1 512-684-1100"
      },
        "address": {
        "address": "1011 W 5th St",
        "postalCode": "1011",
        "countryCode": "USA",
        "city": "Austin",
        "state": "TX",
        "country": "United States"
      },
        "location": {
        "lat": 40.4255485534668,
        "lng": -3.7075681686401367
      }
      }
    }"""
}
