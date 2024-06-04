from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/difference/", response_model=dict, responses={
    200: {"description": "Successful response", "content": {"application/json": {"example": {"start_date": "2021-05-31", "start_time": "00:00:00", "end_date": "2021-06-01", "end_time": "00:00:00"}}}},
    422: {"description": "Bad Request", "content": {"application/json": {"example": {"detail":[
        {
            "loc": ["query", "start_date"],
            "msg": "Invalid date format. Expected 'YYYY-MM-DD'.",
            "type": "value_error"
        },
        {
            "loc": ["query", "start_time"],
            "msg": "Invalid time format. Expected 'HH:MM:SS'.",
            "type": "value_error"
        },
        {
            "loc": ["query", "end_date"],
            "msg": "Invalid date format. Expected 'YYYY-MM-DD'.",
            "type": "value_error"
        },
        {
            "loc": ["query", "end_time"],
            "msg": "Invalid time format. Expected 'HH:MM:SS'.",
            "type": "value_error"
        }
    ] }}}}
})
def difference_data_time(start_date: str, start_time: str, end_date: str, end_time: str) -> dict:

    """
    Calculates the difference between two dates and times in days, hours, minutes and seconds.

    - **start_date**: Start date in 'YYYY-MM-DD' format
    - **start_time**: Start time in 'HH:MM:SS' format
    - **end_date**: End date in 'YYYY-MM-DD' format
    - **end_time**: End time in 'HH:MM:SS' format

    Returns a dictionary with the difference in days, hours, minutes and seconds.
    """

    try:
        start_str = f'{start_date}T{start_time}'
        end_str = f'{end_date}T{end_time}'
        # Convertirlo a un objecto datetime
        start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM:SS' for time.")
    
    # Calcula la diferencia
    difference = start - end
    total_seconds = difference.seconds
    days = difference.days
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
   

    return {
    "start": start,
    "end": end,
    "difference": {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }
}