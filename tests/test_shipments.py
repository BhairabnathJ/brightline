"""Visible tests for ``GET /shipments``.

These probe the *correct* ``main`` behavior at a coarse level only:
- the happy path returns a list of shipments plus pagination metadata, and
- invalid pagination parameters are rejected with an error naming the parameter.

They deliberately do NOT assert page-boundary continuity (no shipment skipped or
duplicated across consecutive pages) — that boundary property is exactly what
the L1 ticket breaks, and is covered by the hidden suite. Keeping it out here
means these tests stay green on ``main`` and on the L1 branch alike.
"""

from __future__ import annotations


def test_shipments_happy_path_returns_items_and_metadata(client) -> None:
    """A default request returns a page of items with pagination metadata."""
    response = client.get("/shipments")

    assert response.status_code == 200
    body = response.json()

    # Pagination metadata is present and reflects the request defaults.
    assert body["page"] == 1
    assert body["pageSize"] == 20
    assert isinstance(body["total"], int)
    assert body["total"] >= 20  # seed loads >= 20 shipments

    # Items is a list and honors the page size (<= pageSize).
    assert isinstance(body["items"], list)
    assert len(body["items"]) <= body["pageSize"]
    assert len(body["items"]) >= 1


def test_shipments_item_shape(client) -> None:
    """Each returned shipment carries the expected fields."""
    body = client.get("/shipments", params={"page": 1, "pageSize": 5}).json()

    assert len(body["items"]) == 5
    first = body["items"][0]
    for field in ("id", "tracking_code", "origin", "destination", "status", "route_id"):
        assert field in first


def test_shipments_custom_page_size_is_honored(client) -> None:
    """A valid custom pageSize is echoed and bounds the item count."""
    body = client.get("/shipments", params={"page": 1, "pageSize": 3}).json()

    assert body["pageSize"] == 3
    assert len(body["items"]) <= 3


def test_shipments_invalid_page_rejected_naming_parameter(client) -> None:
    """page < 1 is rejected with an error that names ``page`` and no items."""
    response = client.get("/shipments", params={"page": 0})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["parameter"] == "page"
    assert "items" not in body


def test_shipments_oversized_page_size_rejected_naming_parameter(client) -> None:
    """pageSize above the cap (100) is rejected, naming ``pageSize``, no items."""
    response = client.get("/shipments", params={"pageSize": 200})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["parameter"] == "pageSize"
    assert "items" not in body
