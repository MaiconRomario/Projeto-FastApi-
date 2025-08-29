from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import ALGORITHM, SECRET_KEY, oauth2_schema
# type: ignore



def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
        
    finally:
        session.close

def verify_token(token: str = Depends(oauth2_schema), session : Session = Depends(get_session)):
    try:
        dic_inf = jwt.decode(token, SECRET_KEY, ALGORITHM)  # type: ignore
        user_id = int(dic_inf.get("sub")) # type: ignore
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied")
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid access")
    return user
