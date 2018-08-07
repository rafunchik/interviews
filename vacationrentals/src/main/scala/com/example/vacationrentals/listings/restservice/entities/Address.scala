package com.example.vacationrentals.listings.restservice.entities



case class Address(address: String,
                   postalCode: Option[String],
                   countryCode: String,
                   city: String,
                   state: Option[String],
                   country: String)
