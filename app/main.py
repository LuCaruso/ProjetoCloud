from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas, crud, auth, utils
from .database import SessionLocal, engine
from jose import JWTError, jwt

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependência para verificar o token JWT e retornar o usuário
async def get_current_user(token: str = Header(None), db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(status_code=403, detail="Token não fornecido")

    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=403, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")

    # Aqui você pode buscar o usuário no banco de dados se necessário
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=403, detail="Usuário não encontrado")
    return user  # Retorna o objeto do usuário

@app.post("/registrar/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email já registrado")
    # Cria o usuário
    new_user = crud.create_user(db=db, user=user)
    # Gera o token JWT
    access_token = auth.create_access_token(data={"sub": new_user.email})
    # Retorna o token JWT
    return {"jwt": access_token}

@app.post("/login/")
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=user_login.email)
    if not user:
        raise HTTPException(status_code=401, detail="Email não encontrado")
    if not pwd_context.verify(user_login.senha, user.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"jwt": access_token}

@app.get("/consultar/")
def consultar_cotacao(empresa: str, token: str = Header(None), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        current_user = crud.get_user_by_email(db, email=payload["sub"])
        if not current_user:
            raise HTTPException(status_code=403, detail="Usuário não encontrado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido")

    cotacao_info = utils.get_stock_price(empresa)
    if not cotacao_info:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    return {
        "usuario": current_user.nome,
        "empresa": cotacao_info["company_name"],
        "Ticker": empresa,
        "cotacao_atual": cotacao_info["closing_price"],
        "pe_ratio": cotacao_info["pe_ratio"],
        "dividend_yield": cotacao_info["dividend_yield"],
        "market_cap": cotacao_info["market_cap"],
        "roe": cotacao_info["roe"]
    }
