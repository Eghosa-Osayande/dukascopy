from datetime import datetime, timedelta
from dataclasses import asdict
from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

from .interfaces import Timestamped, Candle, Tick, TimeUnit, OfferSide


def slice_by_time(data: list[Timestamped], start: datetime, end: datetime) -> list:
    def lower_bound(target):
        lo, hi = 0, len(data)
        while lo < hi:
            mid = (lo + hi) // 2
            if data[mid].timestamp < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    return data[lower_bound(start) : lower_bound(end)]


def bucket(dt: datetime, interval: int, time_unit: TimeUnit) -> datetime:
    if time_unit == TimeUnit.MONTH:
        month = (dt.month - 1) // interval * interval + 1
        return dt.replace(
            year=dt.year,
            month=month,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

    if time_unit == TimeUnit.WEEK:
        monday = dt.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
            days=dt.weekday()
        )
        epoch = datetime(1970, 1, 5, tzinfo=dt.tzinfo)
        weeks = (monday - epoch).days // 7
        return epoch + timedelta(weeks=(weeks // interval) * interval)

    if time_unit == TimeUnit.DAY:
        origin = datetime(1970, 1, 1, tzinfo=dt.tzinfo)
        days = (dt - origin).days
        return origin + timedelta(days=(days // interval) * interval)

    seconds = {
        TimeUnit.HOUR: 3600,
        TimeUnit.MINUTE: 60,
        TimeUnit.SECOND: 1,
    }.get(time_unit)

    if seconds is None:
        raise ValueError(f"Unsupported time unit: {time_unit}")

    size = interval * seconds
    ts = int(dt.timestamp())
    return datetime.fromtimestamp(ts // size * size, tz=dt.tzinfo)


def aggregate_candles(
    data: list[Candle],
    interval: int,
    time_unit: TimeUnit,
) -> list[Candle]:
    if interval <= 0:
        raise ValueError("Interval must be positive")

    result: list[Candle] = []
    agg = None
    key = None

    for d in data:
        new_key = bucket(d.timestamp, interval, time_unit)

        if key != new_key:
            key = new_key
            agg = Candle(
                timestamp=key,
                open=d.open,
                high=d.high,
                low=d.low,
                close=d.close,
                volume=d.volume,
                time_unit=time_unit,
                interval=interval,
            )
            result.append(agg)
            continue

        agg.high = max(agg.high, d.high)
        agg.low = min(agg.low, d.low)
        agg.close = d.close
        agg.volume += d.volume

    return result


def aggregate_ticks(
    data: list[Tick],
    interval: int,
    time_unit: TimeUnit,
    offer_side: OfferSide,
) -> list[Candle]:
    if interval <= 0:
        raise ValueError("Interval must be positive")

    result: list[Candle] = []
    agg = None
    key = None

    for d in data:
        new_key = bucket(d.timestamp, interval, time_unit)
        price = d.bid if offer_side == OfferSide.BID else d.ask
        volume = d.bid_volume if offer_side == OfferSide.BID else d.ask_volume

        if key != new_key:
            key = new_key
            agg = Candle(
                timestamp=key,
                open=price,
                high=price,
                low=price,
                close=price,
                volume=volume,
                interval=interval,
                time_unit=time_unit,
            )
            result.append(agg)
            continue

        agg.high = max(agg.high, price)
        agg.low = min(agg.low, price)
        agg.close = price
        agg.volume += volume

    return result


def round_candles(candles: Iterable[Candle], round_digits: int):
    for candle in candles:
        candle.open = round(candle.open, round_digits)
        candle.high = round(candle.high, round_digits)
        candle.low = round(candle.low, round_digits)
        candle.close = round(candle.close, round_digits)
    


def to_dataframe(
    data: Iterable[Candle] | Iterable[Tick],
) -> "pd.DataFrame":
    try:
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "pandas is required for DataFrame conversion. "
            "Install it with `pip install pandas`."
        ) from exc

    rows = [asdict(item) for item in data]

    df = pd.DataFrame(rows)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            utc=True,
        )
        df.set_index("timestamp", inplace=True)

    return df
