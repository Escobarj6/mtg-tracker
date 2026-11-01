"""Client for the Scryfall API. All Scryfall traffic goes through this module."""

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Self

import httpx

BASE_URL = "https://api.scryfall.com"
USER_AGENT = "mtg-tracker/0.1 (+https://github.com/Escobarj6/mtg-tracker)"
MIN_INTERVAL = 0.1  # seconds between requests; Scryfall asks for 50-100 ms
# Scryfall's maximum identifiers per /cards/collection request
COLLECTION_BATCH_SIZE = 75


class RateLimiter:
    """Spaces calls at least `interval` seconds apart, safely across threads."""

    def __init__(
        self,
        interval: float,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._interval = interval
        self._clock = clock
        self._sleep = sleep
        self._lock = threading.Lock()
        self._next_allowed = 0.0

    def wait(self) -> None:
        with self._lock:
            now = self._clock()
            if now < self._next_allowed:
                self._sleep(self._next_allowed - now)
                now = self._next_allowed
            self._next_allowed = now + self._interval


class ScryfallError(Exception):
    """Raised when Scryfall keeps refusing requests."""


@dataclass
class CollectionResult:
    cards: list[dict[str, Any]]
    not_found: list[dict[str, Any]]


class ScryfallClient:
    def __init__(
        self,
        transport: httpx.BaseTransport | None = None,
        limiter: RateLimiter | None = None,
        max_retries: int = 3,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._http = httpx.Client(
            base_url=BASE_URL,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=httpx.Timeout(10.0),
            transport=transport,
        )
        self._limiter = limiter or RateLimiter(MIN_INTERVAL)
        self._max_retries = max_retries
        self._sleep = sleep

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()

    def fetch_collection(self, identifiers: list[dict[str, str]]) -> CollectionResult:
        """Look up many cards by set and collector number, 75 per request."""
        result = CollectionResult(cards=[], not_found=[])
        for start in range(0, len(identifiers), COLLECTION_BATCH_SIZE):
            batch = identifiers[start : start + COLLECTION_BATCH_SIZE]
            body = self._request(
                "POST", "/cards/collection", json={"identifiers": batch}
            )
            result.cards.extend(body["data"])
            result.not_found.extend(body["not_found"])
        return result

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        for attempt in range(self._max_retries + 1):
            self._limiter.wait()
            response = self._http.request(method, path, **kwargs)
            if response.status_code != 429:
                response.raise_for_status()
                return response.json()
            if attempt < self._max_retries:
                self._sleep(self._retry_delay(response, attempt))
        raise ScryfallError(
            f"Scryfall rate limit: gave up after {self._max_retries} retries"
        )

    @staticmethod
    def _retry_delay(response: httpx.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After", "")
        if retry_after.isdigit():
            return float(retry_after)
        return float(2**attempt)
