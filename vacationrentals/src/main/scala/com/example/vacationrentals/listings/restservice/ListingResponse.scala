package com.example.vacationrentals.listings.restservice

import com.example.vacationrentals.listings.restservice.entities.{Address, Contact, Location}


case class ListingRepresentation(id: String,
                                 contact: Contact,
                                 address: Address,
                                 location: Location)

case class ListingResponse(listing: ListingRepresentation)
