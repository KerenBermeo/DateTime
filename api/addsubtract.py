from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/addsubtract/")
def add_subtract_time(date_str: str, amount: Union[int, float], unit: str, operation: str) -> dict:
    """
    Add or subtract a specified amount of time (days, weeks, or years) from a given date.

    Parameters:
    - date_str (str): The base date in the format 'YYYY-MM-DD'.
    - amount (Union[int, float]): The amount of time to add or subtract.
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
        raise HTTPException(status_code=400, detail="Invalid date format. Expected 'YYYY-MM-DD'.")

    # Asegurarse de que el amount es un número
    try:
        num = int(amount)
    except ValueError:
        raise HTTPException(status_code=400, detail="Amount must be an integer or float.")

    # Validar operación y unidad
    if operation not in ["add", "subtract"]:
        raise HTTPException(status_code=400, detail="Operation must be 'add' or 'subtract'.")
    if unit not in ["days", "weeks", "years"]:
        raise HTTPException(status_code=400, detail="Unit must be 'days', 'weeks', or 'years'.")

    if unit == "days":
        delta = timedelta(days=num)
    elif unit == "weeks":
        delta = timedelta(weeks=num)
    elif unit == "years":
        try:
            new_year = date.year + num if operation == "add" else date.year - num
            result_date = date.replace(year=new_year)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date operation resulting in an invalid date.")
    else:
        delta = None  # This line should never be reached because of the earlier validation check for unit

    # For 'days' and 'weeks', apply the delta directly
    if unit in ["days", "weeks"]:
        if operation == "add":
            result_date = date + delta
        else:  # operation == "subtract"
            result_date = date - delta

    # Formatear las fechas como ISO 8601
    original_date_iso = date.isoformat()
    result_date_iso = result_date.isoformat()

    return {
        "original": original_date_iso,
        "amount": amount,
        "unit": unit,
        "result": result_date_iso
    }
