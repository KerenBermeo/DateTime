from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/weeknumber_iso/", response_model=dict, responses={
    200: {"description": "Successful response", "content": {"application/json": {"example": {"date": "2021-05-31","week_number": 22}}}},
    422: {"description": "Validation Error", "content":{"application/json": {
        "example": {
            "detail": [
                {
                    "loc": ["query", "date"],
                    "msg": "Invalid date and time format. 'YYYY-MM-DD' expected.",
                    "type": "value_error"
                }
            ]
        }
    }}}
})
def ISO_week_number(date_str:str) -> dict:
    """
    Gets the week number for a given date in 'YYYY-MM-DD' format.

    - **date_str**: Date in 'YYYY-MM-DD' format

    Returns a dictionary with the date and the corresponding week number.
    """

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        _, week, _ = date.isocalendar()

    except ValueError:
         raise HTTPException(status_code=422, detail="Invalid date format. Expected 'YYYY-MM-DD'.")

    return {
    "date": date,
    "week_number": week
    }