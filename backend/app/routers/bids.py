from fastapi import APIRouter

router = APIRouter(prefix="/bids", tags=["Bids"])

@router.get("/")
async def get_bids():
    return {"bids": []}