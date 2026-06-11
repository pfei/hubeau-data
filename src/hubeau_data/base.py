"""Base class for all Hub'Eau API clients."""

from typing import Any

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
