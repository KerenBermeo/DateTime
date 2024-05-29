from fastapi import APIRouter

router = APIRouter()

@router.get("/nextoccurrence/")
def read_endpoint1():
    return {"message": "This is endpoint is nextoccurrence"}