from datetime import datetime, timedelta
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from fastapi import HTTPException
from .crud import get_user_by_id
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    iat = datetime.utcnow()
    to_encode.update({"iat": iat})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db, id: int, senha: str):
    user = get_user_by_id(db, id)
    if not user or not pwd_context.verify(senha, user.senha):
        raise HTTPException(status_code=401, detail="Senha ou email incorretos")
    return user

