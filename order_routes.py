# type: ignore
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema, OrderItemSchema
from models import Order, User, OrderItems

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

@order_router.get('/list')
async def order_list(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if user.admin is not True:
        raise HTTPException(status_code=401, detail='You are not authorized to order list')
    else:
        order_list = session.query(Order).all()
        return {
            'order': order_list
        }

@order_router.post('/order/insert_item/{order_id}') 
async def insert_order_item(order_id: int ,order_item_schema: OrderItemSchema, session : Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    elif not user.admin and user.id != order.user_id: # type: ignore
        raise HTTPException(status_code=403, detail="You are not authorized")
    order_item = OrderItems(order_item_schema.quantity, order_item_schema.flavor, order_item_schema.size, order_item_schema.unit_price, order_id)
    session.add(order_item)
    order.calculate_price()
    session.commit()
    return {
        "message" : "Item creation successful",
        "item_id" : order_item.id,
        "price" : order.price
    }
    

@order_router.post('/order/remove_item/{oder_item_id}') 
async def remove_order_item(oder_item_id: int, session : Session = Depends(get_session), user: User = Depends(verify_token)):
    order_item = session.query(OrderItems).filter(OrderItems.id==oder_item_id).first()
    order = session.query(Order).filter(Order.id==order_item.order_id).first() 
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    elif not user.admin and user.id != order.user_id: 
        raise HTTPException(status_code=403, detail="You are not authorized")
    session.delete(order_item)
    order.calculate_price() 
    session.commit()
    return {
        "message" : "Item removed successfully",
        "quantity_order_item": len(order.items),
        "order": order
    }
    

@order_router.post("/order/finish/{order_id}")
async def finish_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='order not found')
    if not user.admin and user.id != order.user_id:  # type: ignore
        raise HTTPException(status_code=401, detail="You are not authorized to modify")
    order.status ="FINALIZADO"
    session.commit()
    return {
        'message': f'Order {order.id} finish with success',
        'order': order
    }

@order_router.get('/order/{order_id}')
async def view_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail='order not found')
    if not user.admin and user.id != order.user_id:  # type: ignore
        raise HTTPException(status_code=401, detail="You are not authorized to modify")

    return {
        'quantity_item' : len(order.items),
        'order': order
    }

@order_router.get('/list/order-user')
async def order_list(session: Session = Depends(get_session), user: User = Depends(verify_token)):
        order_list = session.query(Order).filter(Order.user_id==user.id).all()
        return {
            'order': order_list
        }

