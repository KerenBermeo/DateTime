from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/addsubtract/", response_model=dict, responses={
    200: {"description": "Successful response", "content": {"application/json": {"example": {"original": "2021-05-31T00:00:00", "amount": 5, "unit": "days", "result": "2021-06-05T00:00:00"}}}},
    422: {"description": "Validation Error", "content": {"application/json": {
    "example": {
        "detail": [
            {
                "loc": ["query", "date_str"],
                "msg": "Invalid date format. Expected 'YYYY-MM-DD'.",
                "type": "value_error"
            },
            {
                "loc": ["query", "amount"],
                "msg": "Amount must be an integer or float.",
                "type": "value_error"
            },
            {
                "loc": ["query", "operation"],
                "msg": "Operation must be 'add' or 'subtract'.",
                "type": "value_error"
            },
            {
                "loc": ["query", "unit"],
                "msg": "Unit must be 'days', 'weeks', or 'years'.",
                "type": "value_error"
            }
        ]
    }
}}}
})
def add_subtract_time(date_str: str, amount: Union[int, float], unit: str, operation: str) -> dict:
    """
    Add or subtract a specified amount of time (days, weeks, or years) from a given date.

    Parameters:
    - date_str (str): The base date in the format 'YYYY-MM-DD'.
    - amount (Union[int, float]): The amount of time to add or subtract (can be integer or float for days/weeks).
    - unit (str): The unit of time to add or subtract (days, weeks, or years).
    - operation (str): The operation to perform. Must be 'add' or 'subtract'.

    Returns:
    - dict: The resulting date after adding or subtracting the specified time in a detailed format.

    Raises:
    - HTTPException: If the date format is incorrect, the unit is invalid, or the operation is invalid.
    """
    try:
        # Convertir el string de fecha a un objeto datetime
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format. Expected 'YYYY-MM-DD'.")

    # Validar que amount sea un número (int o float)
    try:
        num = float(amount)
    except ValueError:
        raise HTTPException(status_code=422, detail="Amount must be an integer or float.")

    # Validar operación y unidad
    if operation not in ["add", "subtract"]:
        raise HTTPException(status_code=422, detail="Operation must be 'add' or 'subtract'.")
    if unit not in ["days", "weeks", "years"]:
        raise HTTPException(status_code=422, detail="Unit must be 'days', 'weeks', or 'years'.")

    if unit == "days":
        delta = timedelta(days=num)
    elif unit == "weeks":
        delta = timedelta(weeks=num)
    elif unit == "years":
        try:
            new_year = date.year + num if operation == "add" else date.year - num
            # Asegurarnos de que el año sea un entero
            result_date = date.replace(year=int(new_year))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date operation resulting in an invalid date.")
    else:
        delta = None  # Nunca se alcanzará por la validación anterior

    # Para 'days' y 'weeks', aplicar el delta directamente
    if unit in ["days", "weeks"]:
        result_date = date + delta if operation == "add" else date - delta

    # Formatear las fechas como ISO 8601
    original_date_iso = date.isoformat()
    result_date_iso = result_date.isoformat()

    return {
        "original": original_date_iso,
        "amount": num if num.is_integer() else num,  # Devuelve int si es .0
        "unit": unit,
        "result": result_date_iso
    }