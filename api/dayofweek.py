from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/dayofweek/", response_model=dict, responses={
    200: {"description": "Successful response", "content": {"application/json": {"example": {"date": "2024-05-28", "day_of_week": "Lunes"}}}},
    422: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "Formato de fecha inválido. Se esperaba 'YYYY-MM-DD' para la fecha."}}}}
})
def day_of_week(date_str: str) -> dict:

    """
    Returns the day of the week corresponding to a specified date.

    Parameters:
    - date_str (str): The date in the format 'YYYY-MM-DD'.

    Returns:
    - dict: A dictionary containing the date and day of the week.

    Usage Example:
    ```
    /dayofweek?date_str=2024-05-28
    ```

    Exceptions:
    - HTTPException: If the date format is incorrect.
    """

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        day = date.weekday()
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        name_day_of_week = days[day]
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Se esperaba 'YYYY-MM-DD' para la fecha.")

    return {
    "date": date,
    "day_of_week": name_day_of_week
    }