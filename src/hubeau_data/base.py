"""Base class for all Hub'Eau API clients."""

from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx

from hubeau_data.retry import hubeau_retry


class HubeauBaseAPI:
    """
    Base class providing a shared HTTP client with retry logic.
    All Hub'Eau API classes should inherit from this.
    """

    DEFAULT_TIMEOUT: float = 30.0

    @hubeau_retry
    def _get(self, url: str, params: dict[str, Any] | None = None) -> httpx.Response:
        """GET request with automatic retry on transient errors."""
        resp = httpx.get(url, params=params or {}, timeout=self.DEFAULT_TIMEOUT)
        resp.raise_for_status()
        return resp

    @staticmethod
    def _extract_next_cursor(next_url: str | None) -> str | None:
        if not next_url:
            return None
        qs = parse_qs(urlparse(next_url).query)
        if "cursor" in qs:
            return qs["cursor"][0]
        if "page" in qs:
            return qs["page"][0]
        return None
