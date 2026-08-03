from collections.abc import Mapping


def get_health_status() -> Mapping[str, str]:
    """Return the public status of the API."""
    return {"status": "ok"}
