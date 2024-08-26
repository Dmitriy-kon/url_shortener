from datetime import UTC, datetime

from app.utils.datetime_provide import SystemDateTime, Timezone

timezones_with_offsets = [
    (Timezone.UTC, 0),
    (Timezone.GMT, 0),
    (Timezone.CET, 1),
    (Timezone.EET, 2),
    (Timezone.MSK, 3),
    (Timezone.IST, 5.5),
    (Timezone.WIB, 7),
    (Timezone.CST, 8),
    (Timezone.JST, 9),
    (Timezone.AEST, 10),
    (Timezone.NZST, 12),
]


def test_get_current_time():
    res = SystemDateTime(Timezone.UTC).get_current_time()
    assert isinstance(res, datetime)
    assert abs((res - datetime.now(tz=UTC)).total_seconds()) < 1


def test_timezone() -> None:
    for timez in Timezone:
        system_time = SystemDateTime(timez).get_current_time()
        expected_time = datetime.now(tz=UTC).astimezone(timez.value)

        assert (
            abs((system_time - expected_time).total_seconds()) < 1
        ), f"Failed for timezone {timez.name}: {system_time} != {expected_time}"
