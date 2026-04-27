from fastapi import APIRouter

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/")
async def get_payments():
    return {"payments": []}