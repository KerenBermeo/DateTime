from fastapi import APIRouter

router = APIRouter()

@router.get("/dayofweek/")
def read_endpoint1():
    return {"message": "This is endpoint is dayofweek"}