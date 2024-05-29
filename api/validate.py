from fastapi import APIRouter

router = APIRouter()

@router.get("/validate/")
def read_endpoint1():
    return {"message": "This is endpoint is validate"}