from pydantic import BaseModel, Field
from typing import Optional


class UsersCreateSchema(BaseModel):
    nome: str
    email: str
    password: str
    administrador: str


class UsersCreateSchemaStatusCod201(BaseModel):
    message: str
    id: str = Field(alias="_id")


class UsersCreateSchemaStatusCod400(BaseModel):
    message: str


class NegativeCreateSchema(BaseModel):
    message: str
    nome: Optional[str]
    email: Optional[str]
    password: Optional[str]
    administrador: Optional[str]


class UserGetByIdBody(BaseModel):
    nome: str
    email: str
    password: str
    administrador: str
    id: str = Field(alias="_id")


class NegativeUserGetById(BaseModel):
    message: str


class UsersGetSchema(BaseModel):
    quantidade: int
    usuarios: list[UserGetByIdBody]


class DeleteUser(BaseModel):
    message: str


class NegativeDeleteUser(BaseModel):
    message: str
    idCarrinho: str


class UpdateUserEmailOld(BaseModel):
    message: str


class UpdateUserEmailNew(BaseModel):
    message: str
    id: str = Field(alias="_id")


class NegativeUpdateUser(BaseModel):
    message: str
