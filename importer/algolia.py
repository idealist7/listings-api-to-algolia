from typing import Any
from datetime import datetime

from algoliasearch.search.client import SearchClientSync

from importer.config import algolia_api_key, algolia_app_id, algolia_index_name

import logging

log = logging.getLogger(__name__)

_client: SearchClientSync | None = None


def get_client() -> SearchClientSync:
    global _client
    if _client is None:
        _client = SearchClientSync(app_id=algolia_app_id(), api_key=algolia_api_key())
    return _client


def index_object(listing: dict[str, Any]) -> None:
    log.info("Indexing listing %s", listing["id"])
    # Algolia uses objectID and not id
    listing["objectID"] = listing["id"]
    del listing["id"]
    if (
        listing["address"]["latitude"] is not None
        and listing["address"]["longitude"] is not None
    ):
        listing["_geoloc"] = {
            "lat": float(listing["address"]["latitude"]),
            "lng": float(listing["address"]["longitude"]),
        }
    listing["updated"] = _iso8601_to_timestamp(listing["updated"])
    listing["expires"] = _iso8601_to_timestamp(listing["expires"])
    listing["starts"] = _iso8601_to_timestamp(listing["starts"])
    listing["ends"] = _iso8601_to_timestamp(listing["ends"])
    get_client().save_object(algolia_index_name(), listing)


def unindex_object(listing_id: str) -> None:
    log.info("Unindexing listing %s", listing_id)
    get_client().delete_object(algolia_index_name(), listing_id)


def _iso8601_to_timestamp(iso_str: str | None) -> int | None:
    if iso_str is None:
        return None
    dt = datetime.fromisoformat(iso_str)
    return int(dt.timestamp())
