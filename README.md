# dukascopy-python

Download historical financial market data from [Dukascopy Bank SA](https://www.dukascopy.com), including tick-level prices and OHLCV candles for Forex, commodities, indices, and other financial instruments.

Supports multiple data feed versions, configurable HTTP sessions, optional logging, and Pandas integration.

## Installation

```bash
pip install dukascopy-python
```

## Backward Compatibility

The previous API remains available through `dukascopy_python.compat`, which uses data feed version 1 internally.

Existing applications can continue using `fetch()`, `live_fetch()`, and legacy constants by updating their imports.

```python
from datetime import datetime, timezone

import dukascopy_python.compat as duka
from dukascopy_python.compat.instruments import (
    INSTRUMENT_FX_MAJORS_EUR_USD,
)

df = duka.fetch(
    INSTRUMENT_FX_MAJORS_EUR_USD,
    duka.INTERVAL_MIN_1,
    duka.OFFER_SIDE_BID,
    datetime(2025, 1, 1, tzinfo=timezone.utc),
    datetime(2025, 1, 2, tzinfo=timezone.utc),
)

df.to_csv("output.csv")
```

## New API

The new API provides two functions:

- `fetch_candles()` — Retrieve historical OHLCV candles.
- `fetch_ticks()` — Retrieve historical bid/ask tick data.

### Fetch Candles

```python
from datetime import datetime, timezone

import dukascopy_python as duka
from dukascopy_python.instruments import I_EUR_USD

candles = duka.fetch_candles(
    instrument=I_EUR_USD,
    interval=1,
    time_unit=duka.TimeUnit.HOUR,
    offer_side=duka.OfferSide.BID,
    start=datetime(2025, 1, 1, tzinfo=timezone.utc),
    end=datetime(2025, 2, 1, tzinfo=timezone.utc),
    version=2,
)

for candle in candles:
    print(candle)
```

### Fetch Ticks

```python
ticks = duka.fetch_ticks(
    instrument=I_EUR_USD,
    start=datetime(2025, 1, 1, tzinfo=timezone.utc),
    end=datetime(2025, 1, 2, tzinfo=timezone.utc),
    version=2,
)

for tick in ticks:
    print(tick)
```

Both functions return iterable model objects.

### Parameters

| Parameter | Description |
|---|---|
| `instrument` | Instrument code, e.g. `I_EUR_USD` |
| `start` | Start datetime (inclusive range boundary, subject to feed behaviour) |
| `end` | End datetime; must be later than `start` |
| `version` | `1` or `2`; defaults to the globally configured version |
| `validate_instrument_name` | Validate and convert the instrument identifier; default `True` |
| `create_session` | Optional callable returning an HTTP session |
| `logger` | Optional `logging.Logger` instance |

Additional parameters for `fetch_candles()`:

| Parameter | Description |
|---|---|
| `interval` | Positive integer specifying the candle interval |
| `time_unit` | `TimeUnit` enum, e.g. `TimeUnit.MINUTE` |
| `offer_side` | `OfferSide.BID` or `OfferSide.ASK` |

`start` and `end` must both be timezone-aware or both timezone-naive. UTC-aware datetimes are recommended.

## Data Feed Versions

Two data feed implementations are available.

| Version | Implementation |
|---|---|
| `1` | `DataFeedV1` (default) |
| `2` | `DataFeedV2` |

### Set the Default Version

```python
duka.set_default_version(2)
```

All subsequent fetch operations use version 2 unless explicitly overridden.

### Override Version Per Request

```python
candles = duka.fetch_candles(
    instrument=I_EUR_USD,
    interval=5,
    time_unit=duka.TimeUnit.MINUTE,
    offer_side=duka.OfferSide.BID,
    start=start,
    end=end,
    version=1,
)
```

The `version` argument overrides the default for that request without changing the global setting.

## Data Models

### Candle

| Field | Description |
|---|---|
| `timestamp` | Candle timestamp |
| `open`, `high`, `low`, `close` | OHLC prices |
| `volume` | Trading volume |
| `time_unit` | Candle time unit |
| `interval` | Candle interval |

### Tick

| Field | Description |
|---|---|
| `timestamp` | Tick timestamp |
| `bid`, `ask` | Bid and ask prices |
| `bid_volume`, `ask_volume` | Bid and ask volumes |
| `volume` | Tick volume |

## Pandas Integration

Convert retrieved candles or ticks into a Pandas DataFrame.

```python
candles = list(duka.fetch_candles(
    instrument=I_EUR_USD,
    interval=1,
    time_unit=duka.TimeUnit.HOUR,
    offer_side=duka.OfferSide.BID,
    start=start,
    end=end,
))

df = duka.to_dataframe(candles)

df.to_csv("candles.csv")
df.to_json("candles.json")
```

Pandas is an optional dependency. Install it with:

```bash
pip install pandas
```

## Advanced Configuration

### Custom HTTP Session

Use the `create_session` argument to provide a session factory.

```python
candles = duka.fetch_candles(
    instrument=I_EUR_USD,
    interval=1,
    time_unit=duka.TimeUnit.HOUR,
    offer_side=duka.OfferSide.BID,
    start=start,
    end=end,
    create_session=lambda: duka.create_session(retries=7),
)
```

The library manages the returned session using a context manager.

### Custom Logging

Provide a configured Python logger:

```python
import logging

logger = duka.create_logger(
    name="dukascopy",
    level=logging.DEBUG,
)

ticks = duka.fetch_ticks(
    instrument=I_EUR_USD,
    start=start,
    end=end,
    logger=logger,
)
```

### Instrument Validation

Instrument validation and identifier conversion are enabled by default.

To bypass them:

```python
ticks = duka.fetch_ticks(
    instrument="EUR/USD",
    start=start,
    end=end,
    version=2,
    validate_instrument_name=False,
)
```

When validation is disabled, the instrument identifier is passed directly to the selected data feed.

## Migration Reference

| Previous API | New API |
|---|---|
| `dukascopy_python.compat` | `dukascopy_python` |
| `fetch()` | `fetch_candles()` / `fetch_ticks()` |
| `live_fetch()` | Available through `compat` |
| `INTERVAL_MIN_1` | `interval=1, time_unit=TimeUnit.MINUTE` |
| `OFFER_SIDE_BID` | `OfferSide.BID` |
| `INSTRUMENT_FX_MAJORS_EUR_USD` | `I_EUR_USD` |
| Pandas DataFrame | Iterable `Candle` / `Tick` objects |

## License

MIT

## Contributing

Contributions, bug reports, and pull requests are welcome.
