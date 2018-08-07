package com.example.vacationrentals.listings.restservice.entities


sealed trait CountryCode

//ISO alpha-2 codes, just 3 included as a demo version :)
object CountryCode {
  object UK extends CountryCode
  object US extends CountryCode
}

