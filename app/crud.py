from sqlalchemy.orm import Session
from . import models
from . import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    senha = pwd_context.hash(user.senha)
    db_user = models.User(nome=user.nome, email=user.email, senha=senha)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

