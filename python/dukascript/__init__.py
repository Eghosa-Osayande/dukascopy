import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import random
import string
from time import sleep
import logging

TIME_UNIT_MONTH = "MONTH"
TIME_UNIT_WEEK = "WEEK"
TIME_UNIT_DAY = "DAY"
TIME_UNIT_HOUR = "HOUR"
TIME_UNIT_MIN = "MIN"
TIME_UNIT_SEC = "SEC"
TIME_UNIT_TICK = "TICK"

INTERVAL_MONTH_1 = f"1{TIME_UNIT_MONTH}"
INTERVAL_WEEK_1 = f"1{TIME_UNIT_WEEK}"
INTERVAL_DAY_1 = f"1{TIME_UNIT_DAY}"
INTERVAL_HOUR_4 = f"4{TIME_UNIT_HOUR}"
INTERVAL_HOUR_1 = f"1{TIME_UNIT_HOUR}"
INTERVAL_MIN_30 = f"30{TIME_UNIT_MIN}"
INTERVAL_MIN_15 = f"15{TIME_UNIT_MIN}"
INTERVAL_MIN_10 = f"10{TIME_UNIT_MIN}"
INTERVAL_MIN_5 = f"5{TIME_UNIT_MIN}"
INTERVAL_MIN_1 = f"1{TIME_UNIT_MIN}"
INTERVAL_SEC_30 = f"30{TIME_UNIT_SEC}"
INTERVAL_SEC_10 = f"10{TIME_UNIT_SEC}"
INTERVAL_SEC_1 = f"1{TIME_UNIT_SEC}"
INTERVAL_TICK = TIME_UNIT_TICK

_interval_units = {
    INTERVAL_MONTH_1: TIME_UNIT_MONTH,
    INTERVAL_WEEK_1: TIME_UNIT_WEEK,
    INTERVAL_DAY_1: TIME_UNIT_DAY,
    INTERVAL_HOUR_4: TIME_UNIT_HOUR,
    INTERVAL_HOUR_1: TIME_UNIT_HOUR,
    INTERVAL_MIN_30: TIME_UNIT_MIN,
    INTERVAL_MIN_15: TIME_UNIT_MIN,
    INTERVAL_MIN_10: TIME_UNIT_MIN,
    INTERVAL_MIN_5: TIME_UNIT_MIN,
    INTERVAL_MIN_1: TIME_UNIT_MIN,
    INTERVAL_SEC_30: TIME_UNIT_SEC,
    INTERVAL_SEC_10: TIME_UNIT_SEC,
    INTERVAL_SEC_1: TIME_UNIT_SEC,
    INTERVAL_TICK: TIME_UNIT_TICK,
}

OFFER_SIDE_BID = "B"
OFFER_SIDE_ASK = "A"


def _get_custom_logger(debug=False):
    logger = logging.getLogger("DUKASCRIPT")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    return logger


def _resample_to_nearest(
    timestamp: datetime,
    time_unit: str,
    interval_value: int,
) -> datetime:
    # Round to the nearest time unit based on the interval value
    if time_unit == TIME_UNIT_SEC:
        subtraction = timestamp.second % interval_value
        return timestamp - timedelta(
            seconds=subtraction,
            microseconds=timestamp.microsecond,
        )
    elif time_unit == TIME_UNIT_MIN:
        subtraction = timestamp.minute % interval_value
        return timestamp - timedelta(
            minutes=subtraction,
            seconds=timestamp.second,
            microseconds=timestamp.microsecond,
        )
    elif time_unit == TIME_UNIT_HOUR:
        subtraction = timestamp.hour % interval_value
        return timestamp - timedelta(
            hours=subtraction,
            minutes=timestamp.minute,
            seconds=timestamp.second,
            microseconds=timestamp.microsecond,
        )
    elif time_unit == TIME_UNIT_DAY:
        subtraction = timestamp.day % interval_value
        return timestamp - timedelta(
            days=subtraction,
            hours=timestamp.hour,
            minutes=timestamp.minute,
            seconds=timestamp.second,
            microseconds=timestamp.microsecond,
        )
    elif time_unit == TIME_UNIT_WEEK:
        subtraction = (timestamp.weekday() + 1) % (interval_value * 7)
        return timestamp - timedelta(
            days=subtraction,
            hours=timestamp.hour,
            minutes=timestamp.minute,
            seconds=timestamp.second,
            microseconds=timestamp.microsecond,
        )
    elif time_unit == TIME_UNIT_MONTH:
        month = (timestamp.month // interval_value) + 1
        return datetime(timestamp.year, month, 1, 0, 0, 0, 0, timestamp.tzinfo)
    elif time_unit == TIME_UNIT_TICK:
        return timestamp

    raise NotImplementedError(f"resampling not implemented for {time_unit}")


def _get_dataframe_columns_for_timeunit(time_unit: str) -> list[str]:

    ohlc_df = ["timestamp", "open", "high", "low", "close", "volume"]
    tick_df = ["timestamp", "bidPrice", "askPrice", "bidVolume", "askVolume"]

    df = {
        TIME_UNIT_DAY: ohlc_df,
        TIME_UNIT_HOUR: ohlc_df,
        TIME_UNIT_MIN: ohlc_df,
        TIME_UNIT_MONTH: ohlc_df,
        TIME_UNIT_SEC: ohlc_df,
        TIME_UNIT_TICK: tick_df,
        TIME_UNIT_WEEK: ohlc_df,
    }[time_unit]

    return df


def _fetch(
    instrument: str,
    interval: str,
    offer_side: str,
    last_update: int,
    logger: logging.Logger = logging.getLogger(),
    limit: int = None,
):
    characters = string.ascii_letters + string.digits
    jsonp = f"_callbacks____{''.join(random.choices(characters, k=9))}"

    query_params = {
        "path": "chart/json3",
        "splits": "true",
        "stocks": "true",
        "time_direction": "N",
        "jsonp": jsonp,
        "last_update": f"{int(last_update)}",
        "offer_side": f"{offer_side}",
        "instrument": f"{instrument}",
        "interval": f"{interval}",
    }

    if limit is not None:
        # max limit is 30_000
        query_params["limit"] = f"{int(limit)}"

    base_url = "https://freeserv.dukascopy.com/2.0/index.php"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "Host": "freeserv.dukascopy.com",
        "Referer": "https://freeserv.dukascopy.com/2.0/?path=chart/index&showUI=true&showTabs=true&showParameterToolbar=true&showOfferSide=true&allowInstrumentChange=true&allowPeriodChange=true&allowOfferSideChange=true&showAdditionalToolbar=true&showExportImportWorkspace=true&allowSocialSharing=true&showUndoRedoButtons=true&showDetachButton=true&presentationType=candle&axisX=true&axisY=true&legend=true&timeline=true&showDateSeparators=true&showZoom=true&showScrollButtons=true&showAutoShiftButton=true&crosshair=true&borders=false&freeMode=false&theme=Pastelle&uiColor=%23000&availableInstruments=l%3A&instrument=EUR/USD&period=5&offerSide=BID&timezone=0&live=true&allowPan=true&width=100%25&height=700&adv=popup&lang=en",
    }

    # logger.debug("query params: %s", query_params)

    response = requests.get(base_url, headers=headers, params=query_params)

    jsonText = response.text.removeprefix(f"{jsonp}(").removesuffix(");")

    return json.loads(jsonText)


def _stream(
    instrument: str,
    interval: str,
    offer_side: str,
    start: datetime,
    end: datetime = None,
    max_retries: int = 7,
    limit: int = None,
    logger: logging.Logger = logging.getLogger(),
):
    no_of_retries = 0
    cursor = int(start.timestamp() * 1000)
    end_timestamp = None
    if end is not None:
        end_timestamp = end.timestamp() * 1000

    is_first_iteration = True

    logging.info(f"Start Date :{start.isoformat()}")
    logging.info(f"End Date :{'' if end is None else end.isoformat()}")

    while True:
        try:

            lastUpdates = _fetch(
                instrument=instrument,
                interval=interval,
                offer_side=offer_side,
                last_update=cursor,
                limit=limit,
            )

            if not is_first_iteration and lastUpdates[0][0] == cursor:
                lastUpdates = lastUpdates[1:]

            if len(lastUpdates) < 1:
                if end is not None:
                    break
                else:
                    continue

            for row in lastUpdates:
                if end_timestamp is not None and row[0] > end_timestamp:
                    return
                if interval == INTERVAL_TICK:
                    row[-1] = row[-1] / 1_000_000
                    row[-2] = row[-2] / 1_000_000
                yield row
                cursor = row[0]

            logger.info(
                f"current timestamp :{datetime.fromtimestamp(cursor/1000).isoformat()}"
            )

            no_of_retries = 0
            is_first_iteration = False

        except Exception as e:
            import traceback

            stacktrace = traceback.format_exc()
            no_of_retries += 1
            if max_retries is not None and (no_of_retries - 1) > max_retries:
                logger.debug("error fetching")
                logger.debug(e, stacktrace)
                raise e
            else:
                logger.debug("an error occured", e)
                logger.debug(e, stacktrace)
                logger.debug("retrying")
                sleep(1)
            continue


def fetch(
    instrument: str,
    interval: str,
    offer_side: str,
    start: datetime,
    end: datetime,
    max_retries: int = 7,
    limit: int = 30_000,  # max 30_000
    debug=False,
):
    logger = _get_custom_logger(debug)
    time_unit = _interval_units[interval]
    columns = _get_dataframe_columns_for_timeunit(time_unit)

    data = []

    datafeed = _stream(
        instrument=instrument,
        interval=interval,
        offer_side=offer_side,
        start=start,
        end=end,
        max_retries=max_retries,
        limit=limit,
        logger=logger,
    )

    for row in datafeed:
        data.append(row)

    df = pd.DataFrame(data=data, columns=columns)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms",
        utc=True,
    )
    df = df.set_index("timestamp")
    return df


def live_fetch(
    instrument: str,
    interval_value: int,
    time_unit: str,
    offer_side: str,
    start: datetime,
    end: datetime,
    max_retries: int = 7,
    limit: int = 30_000,  # max 30_000
    debug=False,
):
    logger = _get_custom_logger(debug)
    assert interval_value > 0

    # validate time unit
    _resample_to_nearest(
        datetime.now(),
        time_unit,
        interval_value,
    )

    open, high, low, close, volume = None, 0, 0, 0, 0

    price_index = {
        OFFER_SIDE_BID: 1,
        OFFER_SIDE_ASK: 2,
    }[offer_side]

    volume_index = {
        OFFER_SIDE_BID: -2,
        OFFER_SIDE_ASK: -1,
    }[offer_side]

    last_timestamp = None

    columns = _get_dataframe_columns_for_timeunit(time_unit)
    df = pd.DataFrame(columns=columns)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms",
        utc=True,
    )
    df = df.set_index("timestamp")

    datafeed = _stream(
        instrument=instrument,
        interval=INTERVAL_TICK,
        offer_side=offer_side,
        start=start,
        end=end,
        max_retries=max_retries,
        limit=limit,
        logger=logger,
    )

    yield df

    last_tick_count = 0

    for tick_count, row in enumerate(datafeed, 0):

        timestamp = _resample_to_nearest(
            pd.to_datetime(
                row[0],
                unit="ms",
                utc=True,
            ),
            time_unit,
            interval_value,
        )

        if last_timestamp == None:
            last_timestamp = timestamp

        if time_unit == TIME_UNIT_TICK and interval_value == 1:
            df.loc[timestamp] = [
                *row[1:],
            ]
            yield df
            continue

        new_tick_count = tick_count // interval_value

        if (
            time_unit != TIME_UNIT_TICK
            and timestamp.timestamp() != last_timestamp.timestamp()
        ) or (time_unit == TIME_UNIT_TICK and last_tick_count != new_tick_count):
            if open is not None:
                df.loc[last_timestamp] = [
                    open,
                    high,
                    low,
                    close,
                    volume,
                ]

                yield df
            last_timestamp = timestamp
            last_tick_count = new_tick_count
            open = None

        if open is None:
            open = row[price_index]
            close = open
            low = open
            high = open
            volume = 0

        close = row[price_index]
        high = max(high, close)
        low = min(low, close)
        volume += row[volume_index]

        df.loc[timestamp] = [
            open,
            high,
            low,
            close,
            volume,
        ]

        yield df
