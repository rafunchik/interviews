package com.example.vacationrentals.listings.domain

case class Listing(id: String,
                   phone: String,
                   formattedPhone: String,
                   address: String,
                   postalCode: Option[String],
                   countryCode: String,
                   city: String,
                   state: Option[String],
                   country: String,
                   lat: Double,
                   lng: Double)
