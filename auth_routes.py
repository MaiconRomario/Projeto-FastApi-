# type: ignore
from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session, verify_token
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from schemas import UserSchema, LoginSchema 
from sqlalchemy.orm import Session
from jose import jwt, JWSError
from datetime import datetime, timezone, timedelta

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def creating_token(user_id, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    date_expiration = datetime.now(timezone.utc) + duration_token
    dic_info ={"sub": str(user_id), "exp": date_expiration}
    encoded_JWT = jwt.encode(dic_info, SECRET_KEY, ALGORITHM) 
    return encoded_JWT

def user_authentication(email, senha, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(senha, user.password):
        return False
    return user

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
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session : Session = Depends(get_session)):
    user = user_authentication(login_schema.email, login_schema.password,session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or credentials not found ")
    else:
        access_token = creating_token(user.id)
        refresh_token = creating_token(user.id, duration_token=timedelta(days=7) )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type" : "Bearer"
        }
    
@auth_router.get("/refresh")
async def user_refresh_token(user: User = Depends(verify_token)):
    access_token = creating_token(user.id)
    return {
            "access_token": access_token,
            "token_type" : "Bearer"
        }


    