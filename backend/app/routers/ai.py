from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["AI"])

@router.get("/")
async def ai_health():
    return {"status": "ok"}