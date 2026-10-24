# Brightline Logistics

Brightline Logistics is a small shipment-tracking service. It manages three
domain resources — **shipments**, **drivers**, and **routes** — and exposes
them over a JSON HTTP API.

The service is built with [FastAPI](https://fastapi.tiangolo.com/) on Python
3.12 and persists data in a local **SQLite** database. On startup it creates the
schema and seeds a realistic dataset (20+ shipments, several drivers across a
mix of timezones, and the routes that connect them) so the API has data to
serve immediately.

## Domain

- **Shipments** move between an origin and a destination along a route and carry
  a status (`pending`, `in_transit`, `delivered`) and a unique tracking code.
- **Drivers** are assigned to routes and carry an IANA timezone, which is used
  when localizing route arrival times.
- **Routes** have a `distance` (km) and an `average_speed` (km/h), from which the
  travel time is derived.

## Running the app

Install the dependencies and start the development server with uvicorn:

```bash
pip install -e .
uvicorn app.main:app --reload
```

The API is then available at `http://127.0.0.1:8000`. Interactive docs are
served at `http://127.0.0.1:8000/docs`.

To (re)seed the database explicitly:

```bash
python -m app.seed
```

## API

### `GET /health`

Liveness probe. Returns `{"status": "ok"}`.

### `GET /shipments`

Returns a page of shipments together with pagination metadata.

Query parameters:

- `page` — 1-based page number (default `1`).
- `pageSize` — number of shipments per page (default `50`, maximum `100`).

The response body carries the shipments for the requested page plus the `page`,
`pageSize`, and `total` fields. Invalid pagination parameters are rejected with
an error that names the offending parameter.

### `GET /routes/{id}`

Returns a single route, including the computed estimated time of arrival. The
ETA is derived from the route's distance and average speed and localized to the
assigned driver's timezone.

### `GET /routes/{id}/eta`

Returns the estimated time of arrival for the route as a standalone value,
computed from the route's distance and average speed.

## Running the tests

The visible test suite runs with pytest:

```bash
pip install -e ".[dev]"
pytest
```

## Project layout

```
app/
  main.py        FastAPI app and router wiring
  db.py          SQLite engine, session, and schema setup
  models.py      SQLAlchemy models: drivers, routes, shipments
  seed.py        Idempotent seed data
  shipments.py   GET /shipments
  routes.py      GET /routes/{id}
  eta.py         ETA computation helpers
tests/           Visible test suite
```
