from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get('/')
async def get_order():
    return {"message": "Voçe acessou as ordens de pedidos."}
