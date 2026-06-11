"""
Retry policy for Hub'Eau API calls.

Hub'Eau APIs have known stability issues — transient errors (timeouts, 503)
are common. This module provides a shared retry decorator for all API clients.

Policy: 3 attempts, exponential backoff (1s, 2s, 4s), on transient errors only.
"""

import logging

from httpx import ConnectError, HTTPStatusError, ReadTimeout, TimeoutException
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


def _is_transient(exc: BaseException) -> bool:
    """Return True if the exception is a transient network/server error."""
    if isinstance(exc, (ReadTimeout, TimeoutException, ConnectError)):
        return True
    if isinstance(exc, HTTPStatusError):
        return exc.response.status_code in (429, 500, 502, 503, 504)
    return False


hubeau_retry = retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
