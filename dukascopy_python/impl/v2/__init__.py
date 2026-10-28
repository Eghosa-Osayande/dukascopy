from typing import Callable, Iterable
import requests
import json
from urllib.parse import urlunsplit, urlencode
from datetime import datetime, timezone, timedelta


from ...core import (
    DataFeed,
    TimeUnit,
    OfferSide,
    Candle,
    Tick,
    aggregate_candles,
    aggregate_ticks,
    slice_by_time,
    round_candles,
    debug,
)


class ApiV2Error(Exception):
    def __init__(self, response: requests.Response):
        self.response = response
        self.status_code = response.status_code
        self.url = response.url

        message = "An error occurred while making the API request"

        try:
            result = response.json()

            if isinstance(result, dict) and "error" in result:
                error = result["error"]

                if isinstance(error, dict):
                    message = (
                        error.get("message") or error.get("description") or str(error)
                    )
                else:
                    message = str(error)

            elif isinstance(result, dict) and "message" in result:
                message = str(result["message"])

        except ValueError:
            if response.text.strip():
                message = response.text.strip()

        super().__init__(f"HTTP {self.status_code}: {message}")


class ApiV2:

    def __init__(self, session: requests.Session):
        self.session = session

    def get_candles(
        self,
        instrument: str,
        time_unit: TimeUnit,
        offer_side: OfferSide,
        start: datetime | None = None,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        hour: int | None = None,
    ):

        resolved_offer_side = {OfferSide.ASK: "ASK", OfferSide.BID: "BID"}.get(
            offer_side
        )

        resolved_time_unit = {
            TimeUnit.DAY: "day",
            TimeUnit.HOUR: "hour",
            TimeUnit.MINUTE: "minute",
        }.get(time_unit)

        if resolved_time_unit is None:
            ...

        path_segments = [
            f"/v1/candles/{resolved_time_unit}/{instrument}/{resolved_offer_side}",
        ]

        if year is not None:
            path_segments.append(f"{year}")

            if month is not None:
                path_segments.append(f"{month}")

                if day is not None:
                    path_segments.append(f"{day}")

                    if hour is not None:
                        path_segments.append(f"{hour}")

        path = "/".join(path_segments)

        params = {}
        if start is not None:
            params["from"] = int(start.timestamp() * 1000)

        response = self._make_request(
            [
                path,
                urlencode(params),
                "",
            ]
        )

        if response.status_code != 200:
            raise ApiV2Error(response)

        results = json.loads(response.text)

        ohlc_data_list = self._parse_ohlc(results, time_unit=time_unit)

        return ohlc_data_list

    def get_ticks(
        self,
        instrument: str,
        start: datetime | None,
        year: int | None,
        month: int | None,
        day: int | None,
        hour: int | None,
    ):

        path_segments = [
            f"/v1/ticks/{instrument}",
        ]

        if year is not None:
            path_segments.append(f"{year}")

            if month is not None:
                path_segments.append(f"{month}")

                if day is not None:
                    path_segments.append(f"{day}")

                    if hour is not None:
                        path_segments.append(f"{hour}")

        path = "/".join(path_segments)

        params = {}
        if start is not None:
            params["from"] = int(start.timestamp() * 1000)

        response = self._make_request(
            [
                path,
                urlencode(params),
                "",
            ]
        )

        if response.status_code != 200:
            raise ApiV2Error(response)

        results = json.loads(response.text)

        ohlc_data_list = self._parse_ticks(results)

        return ohlc_data_list

    def get_instruments(self):
        response = self._make_request(["/v1/instruments", "", ""])

        if response.status_code != 200:
            raise ApiV2Error(response)

        return json.loads(response.text)

    def get_instrument(self, instrument: str):
        response = self._make_request([f"/v1/instruments/{instrument}", "", ""])

        if response.status_code != 200:
            raise ApiV2Error(response)

        return json.loads(response.text)

    def _make_request(
        self,
        components: list[str],
    ):

        url = urlunsplit(
            [
                "https",
                "jetta.dukascopy.com",
                *components,
            ]
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            # "Origin": "https://chart.dukascopy.com",
            # "Referer": "https://chart.dukascopy.com",
            "Origin": "https://widgets.dukascopy.com",
            "Referer": "https://widgets.dukascopy.com/en/historical-data-export",
            "Priority": "u=2, i",
        }

        debug(url)
        response = self.session.get(url, headers=headers)

        return response

    def _parse_ohlc(self, r: dict, time_unit: TimeUnit) -> list[Candle]:
        t = r["timestamp"]
        m = r["multiplier"]
        shift = r["shift"]

        o, h, l, c = (r["open"], r["high"], r["low"], r["close"])

        result = []

        for dt, do, dh, dl, dc, volume in zip(
            r["times"],
            r["opens"],
            r["highs"],
            r["lows"],
            r["closes"],
            r["volumes"],
        ):
            t += dt * shift
            o += do * m
            h += dh * m
            l += dl * m
            c += dc * m

            result.append(
                Candle(
                    timestamp=datetime.fromtimestamp(
                        t / 1000,
                        tz=timezone.utc,
                    ),
                    open=round(o),
                    high=h,
                    low=l,
                    close=c,
                    volume=volume,
                    time_unit=time_unit,
                    interval=1,
                )
            )

        return result

    def _parse_ticks(self, r: dict) -> list[Tick]:
        t = r["timestamp"]
        m = r["multiplier"]
        ask, bid = r["ask"], r["bid"]

        result = []

        for dt, da, db, av, bv in zip(
            r["times"],
            r["asks"],
            r["bids"],
            r["askVolumes"],
            r["bidVolumes"],
        ):
            t += dt
            ask += da * m
            bid += db * m

            result.append(
                Tick(
                    timestamp=datetime.fromtimestamp(
                        t / 1000,
                        tz=timezone.utc,
                    ),
                    ask=ask,
                    bid=bid,
                    ask_volume=av / 1_000_000,
                    bid_volume=bv / 1_000_000,
                    volume=(av + bv) / 1_000_000,
                )
            )

        return result


class DataFeedV2(DataFeed):

    def __init__(
        self,
        session: requests.Session,
    ):
        self.api = ApiV2(session)

    def _fetch_data(
        self,
        instrument: str,
        time_unit: TimeUnit,
        offer_side: OfferSide,
        start_utc: datetime,
        end_utc: datetime,
        aggregrator: Callable[[Iterable], Iterable] | None,
    ):
        now_utc = datetime.now(timezone.utc)

        data = []

        if (
            time_unit == TimeUnit.MONTH
            or time_unit == TimeUnit.WEEK
            or time_unit == TimeUnit.DAY
        ):

            start_of_year = now_utc.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            )

            cursor = start_utc.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            )

            while cursor <= start_of_year and cursor <= end_utc:
                debug("get ", cursor)
                candles = self.api.get_candles(
                    instrument=instrument,
                    time_unit=TimeUnit.DAY,
                    offer_side=offer_side,
                    start=None if cursor < start_of_year else start_of_year,
                    year=cursor.year if cursor < start_of_year else None,
                )
                data.extend(candles)
                cursor = cursor.replace(year=cursor.year + 1)

        if time_unit == TimeUnit.HOUR:
            start_of_month = now_utc.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )

            cursor = start_utc.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            while cursor <= start_of_month and cursor <= end_utc:
                debug("get ", cursor)
                candles = self.api.get_candles(
                    instrument=instrument,
                    time_unit=TimeUnit.HOUR,
                    offer_side=offer_side,
                    start=None if cursor < start_of_month else start_of_month,
                    year=cursor.year if cursor < start_of_month else None,
                    month=cursor.month if cursor < start_of_month else None,
                )
                data.extend(candles)

                cursor = cursor.replace(
                    year=cursor.year + (cursor.month == 12),
                    month=(cursor.month % 12) + 1,
                )

        if time_unit == TimeUnit.MINUTE:
            start_of_day = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)

            cursor = start_utc.replace(hour=0, minute=0, second=0, microsecond=0)

            while cursor <= start_of_day and cursor <= end_utc:
                debug("get ", cursor)
                candles = self.api.get_candles(
                    instrument=instrument,
                    time_unit=TimeUnit.MINUTE,
                    offer_side=offer_side,
                    start=None if cursor < start_of_day else start_of_day,
                    year=cursor.year if cursor < start_of_day else None,
                    month=cursor.month if cursor < start_of_day else None,
                    day=cursor.day if cursor < start_of_day else None,
                )
                data.extend(candles)

                cursor = cursor + timedelta(days=1)

        if time_unit == TimeUnit.SECOND:
            start_of_hour = now_utc.replace(minute=0, second=0, microsecond=0)

            cursor = start_utc.replace(minute=0, second=0, microsecond=0)

            while cursor <= start_of_hour and cursor <= end_utc:
                debug("get ", cursor)
                candles = self.api.get_ticks(
                    instrument=instrument,
                    start=None if cursor < start_of_hour else start_of_hour,
                    year=cursor.year if cursor < start_of_hour else None,
                    month=cursor.month if cursor < start_of_hour else None,
                    day=cursor.day if cursor < start_of_hour else None,
                    hour=cursor.hour if cursor < start_of_hour else None,
                )
                data.extend(candles)

                cursor = cursor + timedelta(hours=1)
        data = slice_by_time(data, start_utc, end_utc)
        if aggregrator:
            data = aggregrator(data)
        return data

    def fetch_candles(
        self,
        instrument: str,
        interval: int,
        time_unit: TimeUnit,
        offer_side: OfferSide,
        start: datetime,
        end: datetime | None = None,
        **kw,
    ) -> Iterable[Candle]:

        now_utc = datetime.now(timezone.utc)
        start_utc = start.astimezone(timezone.utc)
        end_utc = now_utc

        if end is not None:
            end_utc = end.astimezone(timezone.utc)

        price_scale = 5

        if isinstance(kw.get("price_scale"), int):
            price_scale = kw.get("price_scale")

        def aggregrator(v):
            agg = v

            if time_unit == TimeUnit.SECOND:
                debug("aggregrating", interval, time_unit)
                agg = aggregate_ticks(
                    v,
                    interval,
                    time_unit,
                    offer_side,
                )
            elif not (
                interval == 1
                and time_unit
                in {
                    TimeUnit.DAY,
                    TimeUnit.HOUR,
                    TimeUnit.MINUTE,
                }
            ):
                debug("aggregrating", interval, time_unit)
                agg = aggregate_candles(
                    data,
                    interval,
                    time_unit,
                )

            round_candles(
                agg,
                price_scale,
            )

            return agg

        data = self._fetch_data(
            instrument=instrument,
            offer_side=offer_side,
            time_unit=time_unit,
            end_utc=end_utc,
            start_utc=start_utc,
            aggregrator=aggregrator,
        )
        return data

    def fetch_ticks(
        self,
        instrument: str,
        start: datetime,
        end: datetime | None = None,
    ) -> Iterable[Tick]:
        now_utc = datetime.now(timezone.utc)
        start_utc = start.astimezone(timezone.utc)
        end_utc = now_utc

        if end is not None:
            end_utc = end.astimezone(timezone.utc)

        data = self._fetch_data(
            instrument=instrument,
            offer_side=OfferSide.BID,
            time_unit=TimeUnit.SECOND,
            end_utc=end_utc,
            start_utc=start_utc,
        )

        return data
