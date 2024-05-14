from fastapi import Depends, FastAPI, HTTPException, APIRouter

order_router = APIRouter(
    prefix="/order",
)

@order_router.get("/")
async def order():
    return {"message": "Bu order route buyurtmalar sahifasi"}