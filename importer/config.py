import os


def idealist_auth_token() -> str:
    return os.getenv("IDEALIST_AUTH_TOKEN")


def algolia_index_name() -> str:
    return os.getenv("ALGOLIA_INDEX_NAME")


def algolia_app_id() -> str:
    return os.getenv("ALGOLIA_APP_ID")


def algolia_api_key() -> str:
    return os.getenv("ALGOLIA_API_KEY")


def cron_enabled() -> bool:
    return os.getenv("CRON_ENABLED") == "true"


def wait_seconds() -> float:
    return float(os.getenv("WAIT_SECONDS"))
