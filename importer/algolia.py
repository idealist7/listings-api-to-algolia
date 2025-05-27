import json
import re
from typing import Any
from datetime import datetime

from algoliasearch.search.client import SearchClientSync
from algoliasearch.http.exceptions import RequestException

from importer.config import (
    algolia_api_key,
    algolia_app_id,
    algolia_index_name,
    truncate_to_10kb,
)

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
    try:
        get_client().save_object(algolia_index_name(), listing)
    except RequestException as ex:
        match = re.match(
            r"^Record is too big size=(?P<size>\d+)/(?P<max_size>\d+) bytes\.",
            ex.message,
        )
        if match is None:
            raise
        size = int(match.group("size"))
        max_size = int(match.group("max_size"))
        _truncate_listing(listing, size, max_size)
        get_client().save_object(algolia_index_name(), listing)


def unindex_object(listing_id: str) -> None:
    log.info("Unindexing listing %s", listing_id)
    get_client().delete_object(algolia_index_name(), listing_id)


def _iso8601_to_timestamp(iso_str: str | None) -> int | None:
    if iso_str is None:
        return None
    dt = datetime.fromisoformat(iso_str)
    return int(dt.timestamp())


def _listing_size(listing: dict[str, Any]) -> int:
    return len(json.dumps(listing).encode("utf-8"))


def _truncate_listing(listing: dict[str, Any], size: int, max_size: int) -> None:
    ttl = 1000
    while ttl > 0 and _listing_size(listing) > max_size:
        ttl -= 1
        _truncate_longuest_attribute(listing, size - max_size)


def _truncate_longuest_attribute(listing: dict[str, Any], truncate_by: int) -> None:
    attrs = ["description", "applyText", "directions"]
    longuest = max(
        attrs, key=lambda attr: len(listing[attr]) if listing[attr] is not None else 0
    )
    log.info("Truncating %s of listing %s")
    padding = 20
    listing[longuest] = listing[longuest][: -(truncate_by + padding)]
