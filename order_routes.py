from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import OrderSchema
from models import Order

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get('/')
async def get_order():
    return {"message": "Voçe acessou as ordens de pedidos."}


@order_router.post('/order')
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user_id=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {'message': f"Pedido criado com sucesso. Id do pedido: {new_order.id}"}

