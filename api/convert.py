from fastapi import APIRouter, HTTPException
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
from typing import Optional

router = APIRouter()

@router.get("/convert", response_model=dict, responses={
    200: {"description": "Successful response", "content": {"application/json": {"example": {"original": "2024-05-28T15:00:00-05:00", "from_timezone": "America/Bogota", "to_timezone": "America/Argentina/Buenos_Aires", "converted": "2024-05-28T17:00:00-03:00"}}}},
    422: {"description": "Validation Error", "content": {"application/json": {
        "example": {
            "detail": [
                {
                    "loc": ["query", "date"],
                    "msg": "Invalid date format. Expected 'YYYY-MM-DD'.",
                    "type": "value_error"
                },
                {
                    "loc": ["query", "time"],
                    "msg": "Invalid time format. Expected 'HH:MM:SS'.",
                    "type": "value_error"
                },
                {
                    "loc": ["query", "from_timezone"],
                    "msg": "Invalid source time zone.",
                    "type": "value_error"
                },
                {
                    "loc": ["query", "to_timezone"],
                    "msg": "Invalid target time zone.",
                    "type": "value_error"
                }
            ]
        }
    }}}
})
def convert_timezone(date: str, time: str, from_timezone: str, to_timezone: str) -> dict:
    """
    Converts a specified date and time from one time zone to another.

    Parameters:
    - date (str): The base date in the 'YYYY-MM-DD' format.
    - time (str): The base time in the 'HH:MM:SS' format.
    - from_timezone (str): The original time zone (e.g., 'America/Bogota').
    - to_timezone (str): The time zone to convert to (e.g., 'America/Argentina/Buenos_Aires').

    Returns:
        dict: The converted date and time in the specified time zone.
            Example:
                {
                    "original": "2024-05-28T15:00:00-05:00",
                    "from_timezone": "America/Bogota",
                    "to_timezone": "America/Argentina/Buenos_Aires",
                    "converted": "2024-05-28T17:00:00-03:00"
                }

    Usage Example:
        ```
        /convert?date=2024-05-28&time=15:00:00&from_timezone=America/Bogota&to_timezone=America/Argentina/Buenos_Aires
        ```

    Exceptions:
        HTTPException: If the date or time format is incorrect, or the time zone is invalid.
    """
    try:
        # Validar fecha y hora por separado
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M:%S")
        datetime_str = f"{date}T{time}"
        naive_datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail="Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM:SS' for time."
        )

    try:
        source_timezone = ZoneInfo(from_timezone)
        target_timezone = ZoneInfo(to_timezone)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Invalid time zone. Check available zones here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
        )

    # Asociar zona horaria y convertir
    source_datetime = naive_datetime.replace(tzinfo=source_timezone)
    target_datetime = source_datetime.astimezone(target_timezone)

    return {
        "original": source_datetime.isoformat(),
        "from_timezone": from_timezone,
        "to_timezone": to_timezone,
        "converted": target_datetime.isoformat()
    }