from fastapi import APIRouter

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/")
async def get_reviews():
    return {"reviews": []}