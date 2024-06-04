from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()


@router.get("/current/", response_model=dict, responses={
    200: {"description": "Successful response", "content": {"application/json": {"example": {"unix": 1717002000000, "utc": "Wed, 29 May 2024 12:00:00 GMT", "iso": "2024-05-29T12:00:00Z", "locale": "May 29, 2024, 12:00:00"}}}},
    422: {"description": "Validation Error", "content":{"application/json": {
        "example": {
            "detail": [
                {
                    "loc": ["query", "date"],
                    "msg": "Invalid date and time format. 'YYYY-MM-DDTHH:MM:SS' expected.",
                    "type": "value_error"
                }
            ]
        }
    }}}
})
def current_time(date: str, time: str):
    """
    Returns the current date and time in different formats based on the input provided by the client.

    Parameters:
    - date (str): The date in 'YYYY-MM-DD' format.
    - time (str): The time in 'HH:MM:SS' format.

    Returns:
    - dict: A dictionary containing the current date and time in various formats.

    Usage Example:
    To get the current date and time in different formats:
    ```
    /current/?date=2024-05-31&time=12:00:00
    ```

    Raises:
    - HTTPException: If the date or time format is incorrect.

    """
    try:
        datetime_str = f"{date}T{time}"
        # Convertir la fecha y hora ingresadas por el cliente a un objeto datetime
        input_datetime = datetime.fromisoformat(datetime_str)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date and time format. Expected 'YYYY-MM-DD' for date and 'HH:MM:SS' for time.")

    # Convertir la fecha y hora a formatos solicitados
    unix_time = int(input_datetime.timestamp()) * 1000  # Convertir a milisegundos
    utc_time = input_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")
    iso_time = input_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    locale_time = input_datetime.strftime("%b %d, %Y, %H:%M:%S")

    # Devolver los resultados en un diccionario
    return {
        "unix": unix_time,
        "utc": utc_time,
        "iso": iso_time,
        "locale": locale_time
    }
