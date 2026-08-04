"""Environment-backed application configuration."""

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True, slots=True)
class Settings:
    database_url: str


def get_settings() -> Settings:
    database_url = getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be configured before database access.")
    return Settings(database_url=database_url)
