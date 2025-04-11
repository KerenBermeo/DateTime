from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.get("/format-datetime/", response_model=dict, responses={
    200: {"description": "Successful response", "content": {"application/json": {"example": {
        "unix_ms": 1717002000000,
        "utc_format": "Wed, 29 May 2024 12:00:00 GMT",
        "iso_8601": "2024-05-29T12:00:00",
        "locale_format": "May 29, 2024, 12:00:00"
    }}}},
    422: {"description": "Validation Error", "content": {"application/json": {
        "example": {
            "detail": "Invalid datetime format. Expected 'YYYY-MM-DD' for date and 'HH:MM:SS' for time."
        }
    }}}
})
def format_datetime(
    date: str, 
    time: str,
    timezone: Optional[str] = None
) -> dict:
    """
    Converts a given date and time to multiple standard formats.

    Parameters:
    - date (str): Date in 'YYYY-MM-DD' format.
    - time (str): Time in 'HH:MM:SS' format.
    - timezone (Optional[str]): IANA timezone (e.g., 'America/New_York'). Not yet implemented.

    Returns:
        dict: Converted datetime in formats:
            - unix_ms: Unix timestamp in milliseconds
            - utc_format: RFC 1123 format (e.g., 'Wed, 29 May 2024 12:00:00 GMT')
            - iso_8601: ISO 8601 format without timezone (e.g., '2024-05-29T12:00:00')
            - locale_format: Locale-friendly format (e.g., 'May 29, 2024, 12:00:00')

    Example:
        /format-datetime/?date=2024-05-29&time=12:00:00
    """
    try:
        # Validación estricta del formato
        dt = datetime.strptime(f"{date}T{time}", "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid datetime format. Expected 'YYYY-MM-DD' for date and 'HH:MM:SS' for time."
        )

    # TODO: Implementar manejo de timezone si se necesita
    if timezone:
        raise HTTPException(
            status_code=501,
            detail="Timezone support is not yet implemented."
        )

    return {
        "unix_ms": int(dt.timestamp()) * 1000,
        "utc_format": dt.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "iso_8601": dt.isoformat(),
        "locale_format": dt.strftime("%b %d, %Y, %H:%M:%S")
    }