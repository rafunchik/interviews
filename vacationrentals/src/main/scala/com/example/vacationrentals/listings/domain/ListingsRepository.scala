package com.example.vacationrentals.listings.domain


trait ListingsRepository {
  def put(id: String, listing: Listing): Option[Listing]
  def get(listingId: String): Option[Listing]
  def delete(listingId: String): Option[Listing]
  def putIfabsent(id: String, listing: Listing): Option[Listing]
}
