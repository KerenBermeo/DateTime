from fastapi import APIRouter

router = APIRouter()

@router.get("/difference/")
def read_endpoint1():
    return {"message": "This is endpoint is difference"}