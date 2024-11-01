from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models
from . import schemas
from . import utils
from .auth import SECRET_KEY, ALGORITHM, create_access_token
from .database import SessionLocal, engine
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .crud import get_user_by_id, get_user_by_email, create_user


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Consulta de Cotação de Ações - Cloud 2024.2",
    description="API para consulta de cotações de ações para a disciplina de Computação em Nuvem Insper 2024.2",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Autenticação com Bearer Token (JWT) no header
bearer_scheme = HTTPBearer()

# Dependência para verificar o token JWT e retornar o usuário
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    if token is None:
        raise HTTPException(status_code=403, detail="Token não fornecido")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id= int(payload.get("sub"))
        user = get_user_by_id(db=db, id=id)
        if user.email is None:
            raise HTTPException(status_code=403, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Token inválido")
    # Aqui você pode buscar o usuário no banco de dados se necessário
    if user is None:
        raise HTTPException(status_code=403, detail="Usuário não encontrado")
    return user  # Retorna o objeto do usuário

@app.post("/registrar/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email já registrado")
    # Cria o usuário
    new_user = create_user(db=db, user=user)
    # Gera o token JWT
    access_token = create_access_token(data={"sub": new_user.id, "name":user.nome})
    # Retorna o token JWT
    return {"jwt": access_token}

@app.post("/login/")
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=user_login.email)
    if not user:
        raise HTTPException(status_code=401, detail="Email não encontrado")
    if not pwd_context.verify(user_login.senha, user.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    access_token = create_access_token(data={"sub": user.id, "name":user.nome})
    return {"jwt": access_token}

@app.get("/consultar/")
def consultar_cotacao(empresa: str = "AAPL", current_user: str = Depends(get_current_user)  ):
    try:
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
