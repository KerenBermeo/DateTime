from fastapi import APIRouter

router = APIRouter()

@router.get("/current/")
def read_endpoint1():
    return {"message": "This is endpoint is current"}