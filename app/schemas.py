from pydantic import BaseModel

class UserBase(BaseModel):
    nome: str
    email: str

class UserCreate(UserBase):
    senha: str

class UserLogin(BaseModel):
    email: str
    senha: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
