from typing import Any

import requests

import logging

from importer.config import idealist_auth_token

log = logging.getLogger(__name__)


class IdealistException(Exception):
    pass


class ListingNotFoundException(IdealistException):
    pass


def get_listing_minis(since: str | None) -> tuple[dict[str, Any], bool]:
    log.info("Fetching volops from Idealist.org, since %s", since)
    params = {}
    if since is not None:
        params["since"] = since
        params["includeUnpublished"] = "true"
    headers = {"Accept": "application/json"}
    url = "https://www.idealist.org/api/v1/listings/volops"
    response = requests.get(
        url=url,
        params=params,
        headers=headers,
        auth=(idealist_auth_token(), ""),
    )
    if response.status_code != 200:
        raise IdealistException(
            f"Idealist responded {response.status_code} {response.text}"
        )
    resp_body = response.json()
    return resp_body["volops"], resp_body["hasMore"]


def get_listing_details(listing_id: str) -> dict[str, Any]:
    log.info("Fetching listing from Idealist.org, volop %s", listing_id)
    headers = {"Accept": "application/json"}
    url = f"https://www.idealist.org/api/v1/listings/volops/{listing_id}"
    response = requests.get(
        url=url,
        headers=headers,
        auth=(idealist_auth_token(), ""),
    )
    if response.status_code == 404:
        # has been unpublished since we got the ID
        raise ListingNotFoundException()
    if response.status_code != 200:
        raise IdealistException(
            f"Idealist responded {response.status_code} {response.text}"
        )
    resp_body = response.json()
    return resp_body["volop"]
