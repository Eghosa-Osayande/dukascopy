from typing import Iterable
import requests
import json
import random
import string
from datetime import datetime, timezone


from ...core import TimeUnit, OfferSide, Candle, Tick, DataFeed, debug, get_logger


class ApiV1:
    def __init__(self, session: requests.Session):
        self.session = session

    def get_candles(
        self,
        instrument: str,
        interval: int,
        time_unit: TimeUnit,
        offer_side: OfferSide,
        start: datetime,
        end: datetime | None = None,
        limit: int | None = None,
    ) -> list[Candle]:
        last_update = int(start.timestamp() * 1000)

        side = {OfferSide.ASK: "A", OfferSide.BID: "B"}.get(offer_side)

        unit = {
            TimeUnit.MONTH: "MONTH",
            TimeUnit.WEEK: "WEEK",
            TimeUnit.DAY: "DAY",
            TimeUnit.HOUR: "HOUR",
            TimeUnit.MINUTE: "MIN",
            TimeUnit.SECOND: "SEC",
        }.get(time_unit)

        if unit is None:
            raise ValueError(f"Unsupported time unit: {time_unit}")

        allowed_intervals = {
            TimeUnit.MONTH: {1},
            TimeUnit.WEEK: {1},
            TimeUnit.DAY: {1},
            TimeUnit.HOUR: {1, 4},
            TimeUnit.MINUTE: {1, 5, 10, 15, 30},
            TimeUnit.SECOND: {1, 10, 30},
        }.get(time_unit)

        if interval not in allowed_intervals:
            raise ValueError(f"Unsupported interval: {interval} for {time_unit}")

        results = self._make_request(
            last_update=last_update,
            instrument=instrument,
            interval=f"{interval}{unit}",
            offer_side=side,
            limit=limit,
        )

        return [
            Candle(
                timestamp=datetime.fromtimestamp(
                    timestamp=r[0] / 1000,
                    tz=timezone.utc,
                ),
                open=r[1],
                high=r[2],
                low=r[3],
                close=r[4],
                volume=r[5],
                time_unit=time_unit,
                interval=interval,
            )
            for r in results
            if end is not None and r[0] <= end.timestamp() * 1000
        ]

    def get_ticks(
        self,
        instrument: str,
        offer_side: OfferSide,
        start: datetime,
        end: datetime | None = None,
        limit: int | None = None,
    ) -> list[Tick]:
        last_update = int(start.timestamp() * 1000)

        side = {OfferSide.ASK: "A", OfferSide.BID: "B"}.get(offer_side)

        results = self._make_request(
            last_update=last_update,
            instrument=instrument,
            interval="TICK",
            offer_side=side,
            limit=limit,
        )

        return [
            Tick(
                timestamp=datetime.fromtimestamp(
                    r[0] / 1000,
                    tz=timezone.utc,
                ),
                bid=r[1],
                ask=r[2],
                bid_volume=r[3] / 1_000_000,
                ask_volume=r[4] / 1_000_000,
                volume=(r[3] + r[4]) / 1_000_000,
            )
            for r in results
            if end is not None and r[0] <= end.timestamp() * 1000
        ]

    def _make_request(
        self,
        last_update,
        offer_side,
        instrument,
        interval,
        limit=None,
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

        response = self.session.get(base_url, headers=headers, params=query_params)

        jsonText = response.text.removeprefix(f"{jsonp}(").removesuffix(");")

        results = json.loads(jsonText)
        return results


class DataFeedV1(DataFeed):

    def __init__(
        self,
        session: requests.Session,
    ):

        self.api = ApiV1(session)


    def _fetch_data(
        self,
        instrument: str,
        interval: int,
        time_unit: TimeUnit,
        offer_side: OfferSide,
        start_utc: datetime,
        end_utc: datetime,
        fetch_ticks: bool,
    ):
        logger = get_logger()

        data = []
        cursor = start_utc
        is_first_iteration = True
        batch_count = 0

        total_seconds = (end_utc - start_utc).total_seconds()
        data_type = "ticks" if fetch_ticks else "candles"

        logger.info(
            "Downloading %s | %s | %s to %s",
            instrument,
            data_type,
            start_utc.isoformat(),
            end_utc.isoformat(),
        )

        while True:
            debug("Fetching from", cursor)

            if fetch_ticks:
                results = self.api.get_ticks(
                    instrument=instrument,
                    start=cursor,
                    end=end_utc,
                    offer_side=offer_side,
                    limit=None,
                )
            else:
                results = self.api.get_candles(
                    instrument=instrument,
                    interval=interval,
                    time_unit=time_unit,
                    start=cursor,
                    end=end_utc,
                    offer_side=offer_side,
                    limit=None,
                )

            if not results:
                break

            batch_count += 1

            start_index = 0

            if (
                not is_first_iteration
                and results[0].timestamp == cursor
            ):
                if len(results) == 1:
                    break

                start_index = 1

            previous_cursor = cursor
            is_complete = True

            for item in results[start_index:]:
                if item.timestamp >= end_utc:
                    break

                data.append(item)
                cursor = item.timestamp
            else:
                is_complete = False

            is_first_iteration = False

            # Percentage of requested time range covered.
            elapsed_seconds = (
                cursor - start_utc
            ).total_seconds()

            progress = min(
                100.0,
                max(0.0, elapsed_seconds / total_seconds * 100),
            )

            logger.info(
                "Download progress: %.1f%% | %d batches | "
                "%d records | %s",
                progress,
                batch_count,
                len(data),
                cursor.isoformat(),
            )

            if is_complete:
                break

            # Prevent repeated requests without cursor advancement.
            if cursor <= previous_cursor:
                logger.warning(
                    "Download stopped: cursor did not advance at %s",
                    cursor.isoformat(),
                )
                break

        logger.info(
            "Download complete: %d %s in %d batches",
            len(data),
            data_type,
            batch_count,
        )

        return data

    def fetch_candles(
        self,
        instrument: str,
        interval: int,
        time_unit: TimeUnit,
        offer_side: OfferSide,
        start: datetime,
        end: datetime,
        **kw,
    ) -> Iterable[Candle]:

        start_utc = start.astimezone(timezone.utc)
        end_utc = end.astimezone(timezone.utc)

        data = self._fetch_data(
            instrument=instrument,
            interval=interval,
            offer_side=offer_side,
            time_unit=time_unit,
            end_utc=end_utc,
            start_utc=start_utc,
            fetch_ticks=False,
        )

        return data

    def fetch_ticks(
        self,
        instrument: str,
        start: datetime,
        end: datetime,
    ) -> Iterable[Tick]:
        start_utc = start.astimezone(timezone.utc)
        end_utc = end.astimezone(timezone.utc)

        data = self._fetch_data(
            instrument=instrument,
            interval=1,
            offer_side=OfferSide.BID,
            time_unit=TimeUnit.SECOND,
            end_utc=end_utc,
            start_utc=start_utc,
            fetch_ticks=True,
        )

        return data
