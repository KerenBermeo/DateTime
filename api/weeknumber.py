from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict

router = APIRouter()

@router.get("/weeknumber_iso/", response_model=Dict, responses={
    200: {
        "description": "Successful response", 
        "content": {
            "application/json": {
                "example": {
                    "date": "2021-05-31",
                    "iso_week_number": 22,
                    "iso_year": 2021,
                    "description": "Week 22 of ISO year 2021"
                }
            }
        }
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "loc": ["query", "date"],
                        "msg": "Invalid date format. Expected 'YYYY-MM-DD'.",
                        "type": "value_error"
                    }
                }
            }
        }
    }
})
def get_iso_week_number(date_str: str) -> Dict:
    """
    Get the ISO week number for a given date according to ISO 8601 standard.

    - Uses ISO 8601 week numbering (Week 1 is the week containing the first Thursday of the year)
    - ISO year may differ from calendar year for dates in January or December

    Parameters:
    - date_str (str): Date in 'YYYY-MM-DD' format

    Returns:
        Dictionary containing:
        - date: Original date string
        - iso_week_number: Week number (1-53)
        - iso_year: ISO year (may differ from calendar year)
        - description: Human-readable description

    Example:
        /weeknumber_iso/?date_str=2021-05-31
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail={
                "loc": ["query", "date"],
                "msg": "Invalid date format. Expected 'YYYY-MM-DD'.",
                "type": "value_error"
            }
        )

    iso_year, iso_week, iso_day = date_obj.isocalendar()

    return {
        "date": date_str,
        "iso_week_number": iso_week,
        "iso_year": iso_year,
        "description": f"Week {iso_week} of ISO year {iso_year}"
    }