from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Literal

router = APIRouter()

@router.get("/dayofweek/", response_model=dict, responses={
    200: {"description": "Successful response", "content": {"application/json": {
        "example": {
            "date": "2024-05-28",
            "day_of_week": "Tuesday",
            "day_of_week_es": "Martes",
            "day_number": 2  # 0=Monday, 6=Sunday
        }
    }}},
    422: {"description": "Validation Error", "content": {"application/json": {
        "example": {
            "detail": "Invalid date format. Use 'YYYY-MM-DD'."
        }
    }}}
})
def day_of_week(
    date_str: str,
    language: Literal['en', 'es'] = 'en'
) -> dict:
    """
    Get the day of the week for a given date.

    Parameters:
    - date_str (str): Date in 'YYYY-MM-DD' format.
    - language (str): Output language ('en' for English, 'es' for Spanish). Default 'en'.

    Returns:
        dict: {
            "date": str,          # Original date
            "day_of_week": str,   # Day name in requested language
            "day_of_week_es": str,# Day name in Spanish (always included)
            "day_number": int     # ISO weekday (0=Monday, 6=Sunday)
        }

    Example:
        /dayofweek/?date_str=2024-05-28&language=es
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid date format. Use 'YYYY-MM-DD'."
        )

    days_es = [
        "Lunes", "Martes", "Miércoles",
        "Jueves", "Viernes", "Sábado", "Domingo"
    ]
    days_en = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    day_num = date_obj.weekday()  # 0=Monday, 6=Sunday

    return {
        "date": date_str,  # Mantener el string original
        "day_of_week": days_en[day_num] if language == 'en' else days_es[day_num],
        "day_of_week_es": days_es[day_num],
        "day_number": day_num
    }