import pytest

from mtg_api.services.scryfall import RateLimiter


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
