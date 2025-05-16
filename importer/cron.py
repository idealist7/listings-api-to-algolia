import time
from datetime import datetime, timedelta, timezone

from importer.algolia import index_object, unindex_object
from importer.config import cron_enabled, wait_seconds
from importer.idealist import (
    ListingNotFoundException,
    get_listing_minis,
    get_listing_details,
)
from importer.storage import load_since, save_since

import logging

log = logging.getLogger(__name__)


def import_batch(since: str | None) -> tuple[str | None, bool]:
    new_since = since
    try:
        listing_minis, has_more = get_listing_minis(
            since=since,
        )
        time.sleep(wait_seconds())
        for listing_mini in listing_minis:
            if listing_mini["isPublished"]:
                try:
                    listing_details = get_listing_details(listing_mini["id"])
                    index_object(listing_details)
                except ListingNotFoundException:
                    unindex_object(listing_mini["id"])
                time.sleep(wait_seconds())
            else:
                unindex_object(listing_mini["id"])
            new_since = listing_mini["updated"]
        return new_since, has_more
    except Exception:
        log.exception(
            "Exception while importing listings, latest 'since': %s", new_since
        )
        return new_since, False


def import_cron():
    if not cron_enabled():
        log.info("Cron disabled, skipping")
        return
    since = load_since()
    log.info("Import cron start, since: %s", since)
    # 20 minutes crons, 3 minutes padding
    timeout = datetime.now(timezone.utc) + timedelta(minutes=17)
    has_more = True
    while has_more and datetime.now(timezone.utc) < timeout:
        new_since, has_more = import_batch(since=since)
        if new_since is not None:
            save_since(new_since)
            if has_more:
                assert new_since != since
            since = new_since
    log.info("Import cron end, since for next run: %s", since)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import_cron()
