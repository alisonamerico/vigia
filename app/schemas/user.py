from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telegram_id: int
    nome: str
    cidade: str
    bairro: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserSchema(UserBase):
    id: int
    active: bool = True
