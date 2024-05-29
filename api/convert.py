from fastapi import APIRouter

router = APIRouter()

@router.get("/convert/")
def read_endpoint1():
    return {"message": "This is endpoint is convert"}