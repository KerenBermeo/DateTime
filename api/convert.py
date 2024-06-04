from fastapi import APIRouter, HTTPException
from datetime import datetime
import pytz


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
    - dict: The converted date and time in the specified time zone.

    Usage Example:

    ```
    /convert?date=2024-05-28&time=15:00:00&from_timezone=America/Bogota&to_timezone=America/Argentina/Buenos_Aires
    ```
    
    
    Exceptions:
    - HTTPException: If the date or time format is incorrect, or the time zone is invalid.

    """
    try:
        # Combinar la fecha y la hora en un string datetime y convertirlo a un objeto datetime
        datetime_str = f"{date}T{time}"
        naive_datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM:SS' for time.")

    try:
        # Obtener los objetos de zona horaria
        source_timezone = pytz.timezone(from_timezone)
        target_timezone = pytz.timezone(to_timezone)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(status_code=422, detail="Invalid time zone.")

    # Asociar la zona horaria original al objeto datetime
    source_datetime = source_timezone.localize(naive_datetime)

    # Convertir la fecha y hora a la zona horaria objetivo
    target_datetime = source_datetime.astimezone(target_timezone)

    original_date_iso = source_datetime.isoformat()
    result_date_iso = target_datetime.isoformat()

    return {
        "original": original_date_iso,
        "from_timezone": from_timezone,
        "to_timezone": to_timezone,
        "converted": result_date_iso
    }

