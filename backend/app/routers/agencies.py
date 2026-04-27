from fastapi import APIRouter

router = APIRouter(prefix="/agencies", tags=["Agencies"])

@router.get("/")
async def get_agencies():
    return {"agencies": []}