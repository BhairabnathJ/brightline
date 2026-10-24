"""Visible tests for the route resource ``GET /routes/{id}``.

These probe the *correct* ``main`` behavior at a coarse level only: a known
route returns a payload that includes an application-computed ETA, and an
unknown id returns 404.

They deliberately do NOT assert the non-UTC timezone-localized ETA value (the
L2 ticket breaks exactly that conversion) and do NOT touch ``GET /routes/{id}/eta``
(the L3 feature is intentionally absent on ``main`` and its branch). That keeps
these tests green on ``main`` and on the L2/L3 branches alike.
"""

from __future__ import annotations


def test_get_route_returns_route_with_computed_eta(client) -> None:
    """A known route returns its fields plus a computed, positive ETA."""
    response = client.get("/routes/1")

    assert response.status_code == 200
    body = response.json()

    assert body["id"] == 1
    assert "name" in body
    assert body["distance"] > 0
    assert body["average_speed"] > 0

    # The ETA is application-computed; assert only its coarse correctness
    # (eta_hours = distance / average_speed), NOT any timezone localization.
    assert "eta_hours" in body
    assert body["eta_hours"] > 0
    assert body["eta_hours"] == body["distance"] / body["average_speed"]


def test_get_route_unknown_id_returns_404(client) -> None:
    """An unknown route id yields a 404 not-found response."""
    response = client.get("/routes/999999")

    assert response.status_code == 404
