package com.example.vacationrentals.listings.domain


sealed trait CountryCode

//ISO alpha-2 codes
object CountryCode {
  object UK extends CountryCode
  object US extends CountryCode
}