import os
import json

FILENAME = "/data/db.json"


def load_since() -> str | None:
    if not os.path.isfile(FILENAME):
        return None
    with open(FILENAME, "r", encoding="utf-8") as f:
        db_json = f.read()
    db = json.loads(db_json)
    return db["since"]


def save_since(since: str) -> None:
    db = {"since": since}
    db_json = json.dumps(db)
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.write(db_json)
