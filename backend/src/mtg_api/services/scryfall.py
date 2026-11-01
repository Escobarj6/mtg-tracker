"""Client for the Scryfall API. All Scryfall traffic goes through this module."""

import threading
import time
from collections.abc import Callable

BASE_URL = "https://api.scryfall.com"
USER_AGENT = "mtg-tracker/0.1 (+https://github.com/Escobarj6/mtg-tracker)"
MIN_INTERVAL = 0.1  # seconds between requests; Scryfall asks for 50-100 ms


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
