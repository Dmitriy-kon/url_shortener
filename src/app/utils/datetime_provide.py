from datetime import UTC, datetime, timedelta, timezone
from enum import Enum


class Timezone(Enum):
    UTC = UTC
    GMT = timezone(timedelta(hours=0))
    CET = timezone(timedelta(hours=1))
    EET = timezone(timedelta(hours=2))
    MSK = timezone(timedelta(hours=3))
    IST = timezone(timedelta(hours=5, minutes=30))
    WIB = timezone(timedelta(hours=7))
    CST = timezone(timedelta(hours=8))
    JST = timezone(timedelta(hours=9))
    AEST = timezone(timedelta(hours=10))
    NZST = timezone(timedelta(hours=12))


class SystemDateTime:
    def __init__(self, timezone: Timezone) -> None:
        self._timezone = timezone

    def get_current_time(self) -> datetime:
        return datetime.now(tz=self._timezone.value)
