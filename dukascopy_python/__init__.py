from datetime import datetime
from typing import Iterable, TYPE_CHECKING
from .core import (
    TimeUnit,
    OfferSide,
    Candle,
    Tick,
    to_dataframe,
    create_logger,
    create_session,
)

if TYPE_CHECKING:
    import requests
    from .core import DataFeed


__all__ = [
    "fetch_candles",
    "fetch_ticks",
    "set_default_version",
    "to_dataframe",
    "create_logger",
    "create_session",
    "TimeUnit",
    "OfferSide",
    "Candle",
    "Tick",
]


_default_version = 1


def set_default_version(version: int):
    global _default_version
    if version not in (1, 2):
        raise ValueError(f"Unsupported data feed version: {version}")
    _default_version = version


def _create_data_feed(
    version: int,
    session: requests.Session,
    **kw,
) -> DataFeed:

    if version == 1:
        from dukascopy_python.impl.v1 import DataFeedV1

        return DataFeedV1(session=session)

    if version == 2:
        from dukascopy_python.impl.v2 import DataFeedV2

        return DataFeedV2(session=session)

    raise ValueError(f"Unsupported data feed version: {version}")


def _validate_date_range(start: datetime, end: datetime) -> None:
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise TypeError("start and end must be datetime objects")

    start_aware = start.tzinfo is not None and start.utcoffset() is not None
    end_aware = end.tzinfo is not None and end.utcoffset() is not None

    if start_aware != end_aware:
        raise ValueError("start and end must both be timezone-aware or timezone-naive")

    if start >= end:
        raise ValueError(f"start must be earlier than end: start={start}, end={end}")


def _format_instrument_code(code: str, version: int):
    from .instruments import INSTRUMENT_CODE_TO_DATA

    meta_data = INSTRUMENT_CODE_TO_DATA.get(code)

    if version == 1 and meta_data is not None:
        return meta_data["name"], meta_data

    if version == 2 and meta_data is not None:
        return meta_data["code"], meta_data

    raise ValueError(f"Unsupported data feed version: {version}")


def fetch_candles(
    instrument: str,
    interval: int,
    time_unit: TimeUnit,
    offer_side: OfferSide,
    start: datetime,
    end: datetime,
    *,
    version: int | None = None,
    **kw,
) -> Iterable[Candle]:

    from .core import create_session, get_logger, use_logger

    _validate_date_range(start, end)

    if version is None:
        version = _default_version

    instrument, meta_data = instrument, {}

    if kw.get("validate_instrument_name", True):
        instrument, meta_data = _format_instrument_code(instrument, version)

    create_session_fn = lambda: create_session(retries=7)
    if kw.get("create_session") is not None:
        create_session_fn = kw.get("create_session")

    logger = get_logger()

    if kw.get("logger") is not None:
        logger = kw.get("logger")

    with create_session_fn() as session, use_logger(logger):

        datafeed = _create_data_feed(
            version=version,
            session=session,
            **kw,
        )

        return datafeed.fetch_candles(
            instrument=instrument,
            interval=interval,
            time_unit=time_unit,
            offer_side=offer_side,
            start=start,
            end=end,
            price_scale=meta_data.get("priceScale"),
        )


def fetch_ticks(
    instrument: str,
    start: datetime,
    end: datetime,
    *,
    version: int | None = None,
    **kw,
) -> Iterable[Tick]:
    from .core import create_session, get_logger, use_logger

    _validate_date_range(start, end)

    if version is None:
        version = _default_version

    instrument, meta_data = instrument, {}

    if kw.get("validate_instrument_name", True):
        instrument, meta_data = _format_instrument_code(instrument, version)

    create_session_fn = lambda: create_session(retries=7)
    if kw.get("create_session") is not None:
        create_session_fn = kw.get("create_session")

    logger = get_logger()

    if kw.get("logger") is not None:
        logger = kw.get("logger")

    with create_session_fn() as session, use_logger(logger):

        datafeed = _create_data_feed(
            version=version,
            session=session,
            **kw,
        )

        return datafeed.fetch_ticks(
            instrument=instrument,
            start=start,
            end=end,
        )
