"""Shared pytest fixtures for the visible Brightline suite.

The app reads ``BRIGHTLINE_DB_PATH`` at import time (``app.db``), so we point it
at a throwaway temp SQLite file *before* importing any ``app`` module. The DB is
seeded once per test session with the standard seed data, and a FastAPI
``TestClient`` is provided for the API tests.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

# Create the temp DB path and export it BEFORE importing app modules so that
# app.db picks it up when its module-level engine is constructed.
_TMP_DIR = tempfile.mkdtemp(prefix="brightline-test-")
_DB_PATH = Path(_TMP_DIR) / "test.db"
os.environ["BRIGHTLINE_DB_PATH"] = str(_DB_PATH)


@pytest.fixture(scope="session")
def seeded_db() -> Iterator[None]:
    """Expose the seeded temp DB to tests.

    The actual seeding runs once at import time (below) so its cost is not
    attributed to any individual test's setup phase — that keeps the
    deliberately-slow test (``tests/test_slow.py``) the strictly-slowest entry
    under ``pytest --durations``.
    """
    yield


# Seed once, eagerly, at collection time — outside any fixture — so the one-time
# DB setup cost does not land on a test's reported setup duration.
def _seed_once() -> None:
    from app.seed import run_seed

    run_seed()


_seed_once()


@pytest.fixture()
def client(seeded_db: None):
    """A FastAPI ``TestClient`` against the app backed by the seeded temp DB."""
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
