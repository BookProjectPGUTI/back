import datetime


def get_now(
        days: int | float = 0,
        seconds: int | float = 0,
        microseconds: int | float = 0,
        milliseconds: int | float = 0,
        minutes: int | float = 0,
        hours: int | float = 0,
        weeks: int | float = 0,
) -> datetime.datetime:
    delta = datetime.timedelta(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks
    )
    return datetime.datetime.now(datetime.UTC) + delta
