import json

import httpx
import pytest

from mtg_api.services.scryfall import (
    USER_AGENT,
    RateLimiter,
    ScryfallClient,
    ScryfallError,
)


class FakeClock:
    """A clock tests control by hand. Sleeping advances time instantly."""

    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def time(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def make_limiter(clock: FakeClock) -> RateLimiter:
    return RateLimiter(0.1, clock=clock.time, sleep=clock.sleep)


def test_first_call_does_not_wait():
    clock = FakeClock()
    limiter = make_limiter(clock)

    limiter.wait()

    assert clock.sleeps == []


def test_back_to_back_calls_are_spaced():
    clock = FakeClock()
    limiter = make_limiter(clock)

    limiter.wait()
    limiter.wait()
    limiter.wait()

    assert clock.sleeps == [pytest.approx(0.1), pytest.approx(0.1)]


def test_no_wait_after_enough_time_passes():
    clock = FakeClock()
    limiter = make_limiter(clock)

    limiter.wait()
    clock.now += 0.5
    limiter.wait()

    assert clock.sleeps == []


ONE_CARD = [{"set": "ltc", "collector_number": "1"}]


def collection_response(request: httpx.Request) -> httpx.Response:
    """Fake Scryfall: returns one card per identifier requested."""
    identifiers = json.loads(request.content)["identifiers"]
    cards = [{"id": str(i)} for i in range(len(identifiers))]
    return httpx.Response(200, json={"object": "list", "not_found": [], "data": cards})


def make_client(handler, clock: FakeClock, max_retries: int = 3) -> ScryfallClient:
    return ScryfallClient(
        transport=httpx.MockTransport(handler),
        limiter=make_limiter(clock),
        max_retries=max_retries,
        sleep=clock.sleep,
    )


def test_sends_identifying_headers():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return collection_response(request)

    with make_client(handler, FakeClock()) as client:
        client.fetch_collection(ONE_CARD)

    assert seen[0].headers["User-Agent"] == USER_AGENT
    assert seen[0].headers["Accept"] == "application/json"


def test_batches_identifiers_in_groups_of_75():
    batch_sizes: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        batch_sizes.append(len(json.loads(request.content)["identifiers"]))
        return collection_response(request)

    identifiers = [{"set": "ltc", "collector_number": str(n)} for n in range(100)]
    with make_client(handler, FakeClock()) as client:
        result = client.fetch_collection(identifiers)

    assert batch_sizes == [75, 25]
    assert len(result.cards) == 100


def test_retries_after_429_honoring_retry_after():
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429, headers={"Retry-After": "2"})
        return collection_response(request)

    clock = FakeClock()
    with make_client(handler, clock) as client:
        result = client.fetch_collection(ONE_CARD)

    assert calls == 2
    assert clock.sleeps == [2.0]
    assert len(result.cards) == 1


def test_gives_up_after_max_retries():
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(429)

    with make_client(handler, FakeClock(), max_retries=2) as client:
        with pytest.raises(ScryfallError):
            client.fetch_collection(ONE_CARD)

    assert calls == 3
