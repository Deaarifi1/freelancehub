from fastapi import APIRouter

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.get("/")
async def get_contracts():
    return {"contracts": []}