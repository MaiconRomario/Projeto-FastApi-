from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema
from models import Order, User

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

@order_router.get('/')
async def get_order():
    return {"message": "Voçe acessou as ordens de pedidos."}

@order_router.post('/order')
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user_id=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {'message': f"Pedido criado com sucesso. Id do pedido: {new_order.id}"}

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='order not found')
    if not user.admin and user.id != order.user_id:  # type: ignore
        raise HTTPException(status_code=401, detail="You are not authorized to modify")
    order.status ="CANCELADO"
    session.commit()
    return {
        'message': f'Order {order.id} cancel with success',
        'order': order
    }
    