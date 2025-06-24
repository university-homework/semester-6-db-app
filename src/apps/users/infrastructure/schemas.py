from infrastructure.db.models import BaseModel
from sqlmodel import Field


class UserBaseSchema(BaseModel):
    id: int | None = Field(None, primary_key=True)
    username: str
    password: str
    last_name: str
    first_name: str
    patronymic: str | None = Field(None)


class UserReadSchema(BaseModel):
    id: int | None = Field(None, primary_key=True)
    username: str
    last_name: str
    first_name: str
    patronymic: str | None = Field(None)
