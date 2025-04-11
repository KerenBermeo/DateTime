from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict

router = APIRouter()

@router.get("/difference/", response_model=Dict, responses={
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {
                    "start_datetime": "2021-05-31T00:00:00",
                    "end_datetime": "2021-06-01T00:00:00",
                    "difference": {
                        "total_days": 1,
                        "total_hours": 24,
                        "total_minutes": 1440,
                        "total_seconds": 86400,
                        "breakdown": {
                            "days": 1,
                            "hours": 0,
                            "minutes": 0,
                            "seconds": 0
                        }
                    }
                }
            }
        }
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["query", "start_date"],
                            "msg": "Invalid date format. Expected 'YYYY-MM-DD'.",
                            "type": "value_error"
                        }
                    ]
                }
            }
        }
    }
})
def calculate_datetime_difference(
    start_date: str,
    start_time: str,
    end_date: str,
    end_time: str
) -> Dict:
    """
    Calculate the difference between two datetimes with precise breakdown.

    Parameters:
    - start_date: Start date in 'YYYY-MM-DD' format
    - start_time: Start time in 'HH:MM:SS' format
    - end_date: End date in 'YYYY-MM-DD' format
    - end_time: End time in 'HH:MM:SS' format

    Returns:
        Dictionary containing:
        - start_datetime: ISO format string of start datetime
        - end_datetime: ISO format string of end datetime
        - difference: {
            - total_days: Total difference in days (as float)
            - total_hours: Total difference in hours
            - total_minutes: Total difference in minutes
            - total_seconds: Total difference in seconds
            - breakdown: {
                - days: Integer days component
                - hours: Remaining hours (0-23)
                - minutes: Remaining minutes (0-59)
                - seconds: Remaining seconds (0-59)
            }
        }

    Raises:
        HTTPException: If any datetime parameter has invalid format
    """
    # Validación individual de cada campo
    errors = []
    try:
        start_dt = datetime.strptime(f"{start_date}T{start_time}", "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        errors.append({
            "loc": ["query", "start_date"],
            "msg": "Invalid datetime format. Expected 'YYYY-MM-DD' for date and 'HH:MM:SS' for time.",
            "type": "value_error"
        })
    
    try:
        end_dt = datetime.strptime(f"{end_date}T{end_time}", "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        errors.append({
            "loc": ["query", "end_date"],
            "msg": "Invalid datetime format. Expected 'YYYY-MM-DD' for date and 'HH:MM:SS' for time.",
            "type": "value_error"
        })
    
    if errors:
        raise HTTPException(status_code=422, detail=errors)

    # Validar que end >= start
    if end_dt < start_dt:
        raise HTTPException(
            status_code=400,
            detail="End datetime must be greater than or equal to start datetime"
        )

    # Calcular diferencia
    delta = end_dt - start_dt
    total_seconds = int(delta.total_seconds())
    
    # Descomposición completa
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "start_datetime": start_dt.isoformat(),
        "end_datetime": end_dt.isoformat(),
        "difference": {
            "total_days": round(total_seconds / 86400, 6),
            "total_hours": round(total_seconds / 3600, 6),
            "total_minutes": round(total_seconds / 60, 6),
            "total_seconds": total_seconds,
            "breakdown": {
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds
            }
        }
    }