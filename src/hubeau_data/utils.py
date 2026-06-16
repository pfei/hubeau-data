"""Shared utilities for Hub'Eau API clients."""
from urllib.parse import parse_qs, urlparse


def extract_next_cursor(next_url: str | None) -> str | None:
    """Extract the pagination cursor or page number from a Hub'Eau next URL."""
    if not next_url:
        return None
    qs = parse_qs(urlparse(next_url).query)
    if "cursor" in qs:
        return qs["cursor"][0]
    if "page" in qs:
        return qs["page"][0]
    return None
