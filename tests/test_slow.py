"""The single deliberately-slow test in the visible suite (Requirement 4.5).

This module contains EXACTLY ONE test, and it is intentionally the strictly
slowest test in the whole suite. It is a realistic imperfection a grader's
"flag the slowest test" tooling is meant to surface — a test padded with a
fixed sleep rather than exercising anything meaningful. The sleep is kept modest
(~1s) so the suite still runs fast for the hackathon demo while remaining
strictly slower than every other (sub-millisecond) test.

Do not remove the ``@pytest.mark.slow`` marker or the sleep: they are the signal
the sandbox is designed to carry.
"""

from __future__ import annotations

import time

import pytest

# How long this test deliberately stalls. Comfortably longer than any other
# timing in the suite (including one-time session setup such as DB seeding, and
# the sub-100ms API test calls), so this is guaranteed to be the strictly
# slowest entry under ``pytest --durations``.
_DELIBERATE_SLEEP_SECONDS = 1.5


@pytest.mark.slow
def test_deliberately_slow_is_strictly_slowest() -> None:
    """Intentionally slow placeholder test (see module docstring).

    The ``time.sleep`` below is deliberate: it makes this the strictly-slowest
    test so tooling that flags slow tests has a clear target. It asserts only a
    trivial truth so it always passes.
    """
    # MOCK-free intentional delay — this is the imperfection itself, not setup.
    time.sleep(_DELIBERATE_SLEEP_SECONDS)
    assert True
