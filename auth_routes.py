# type: ignore
from fastapi import APIRouter, Depends
from models import User
from dependencies import get_session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get('/')
async def home():
    return {'message' : 'Voce accesou a rota padrão auth', "autenticado": False}


@auth_router.post('/create_user')
async def create_user(email: str, password: str, name: str,session = Depends(get_session)):
    user = session.query(User).filter(User.email==email).first()
    if user:
        return {'message': "There is already a user with that email"}
    else:
        new_user = User(name, email, password)
        session.add(new_user)
        session.commit()
        return {'message': "User creating success"}
    