package com.example.vacationrentals.listings.repository

import com.example.vacationrentals.listings.domain.{Listing, ListingsRepository}

import scala.collection.concurrent.TrieMap


object ListingsInMemoryRepository {

  def apply(): ListingsInMemoryRepository = {
    def map = TrieMap.empty[String, Listing]
    new ListingsInMemoryRepository(map)
  }

}

case class ListingsInMemoryRepository(private val map: TrieMap[String, Listing]) extends ListingsRepository {

  //TODO add id param?
  override def put(id: String, listing: Listing): Option[Listing] = map.put(id , listing)

  override def get(listingId: String): Option[Listing] = map.get(listingId)

  override def delete(listingId: String): Option[Listing] = map.remove(listingId)

  override def putIfabsent(id: String, listing: Listing): Option[Listing] = map.putIfAbsent(id , listing)
}
