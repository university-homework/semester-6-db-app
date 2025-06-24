from sqlmodel import Field, Relationship

from infrastructure.db.models import BaseModel


class UserModel(BaseModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(None, primary_key=True)
    username: str
    password: str
    last_name: str
    first_name: str
    patronymic: str | None = Field(None)

    members: list['MemberModel'] = Relationship(back_populates='user')
