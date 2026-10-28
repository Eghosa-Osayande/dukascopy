from dataclasses import dataclass
from typing import Iterable, Protocol
from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod



class OfferSide(Enum):
    BID = "bid"
    ASK = "ask"


class TimeUnit(Enum):
    MONTH = "month"
    WEEK = "week"
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    SECOND = "second"


class Timestamped(Protocol):
    @property
    def timestamp(self) -> datetime: ...


@dataclass
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    time_unit: TimeUnit
    interval: int


@dataclass
class Tick:
    timestamp: datetime
    ask: float
    bid: float
    ask_volume: float
    bid_volume: float
    volume: float


class DataFeed(ABC):
    @abstractmethod
    def fetch_candles(
        self,
        instrument: str,
        interval: int,
        time_unit: TimeUnit,
        offer_side: OfferSide,
        start: datetime,
        end: datetime,
        **kw,
    ) -> Iterable[Candle]: ...

    @abstractmethod
    def fetch_ticks(
        self,
        instrument: str,
        start: datetime,
        end: datetime,
        **kw,
    ) -> Iterable[Candle]: ...

    
