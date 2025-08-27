# type: ignore
from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get('/')
async def home():
    return {'message' : 'Voce accesou a rota padrão auth', "autenticado": False}


@auth_router.post('/create_user')
async def create_user(user_schema: UserSchema ,session : Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email of the already registered user")
    else:
        password_encrypted = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, password_encrypted, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {'message': f"User creating success {user_schema.email}"}
    