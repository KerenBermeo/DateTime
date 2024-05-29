from fastapi import APIRouter

router = APIRouter()

@router.get("/weeknumber/")
def read_endpoint1():
    return {"message": "This is endpoint is weeknumber"}