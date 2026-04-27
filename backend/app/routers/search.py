from fastapi import APIRouter

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
async def search():
    return {"results": []}