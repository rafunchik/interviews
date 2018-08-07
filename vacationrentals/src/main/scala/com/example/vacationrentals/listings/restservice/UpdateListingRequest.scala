package com.example.vacationrentals.listings.restservice

import com.example.vacationrentals.listings.restservice.entities.{Address, Contact, Location}


case class UpdateListingRequest(contact: Contact, address: Address, location: Location)
