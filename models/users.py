from typing import Optional, List
from sqlmodel import SQLModel, Relationship, Field

from pydantic import EmailStr,BaseModel

#from models.events import Event

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    password: str
    events: Optional[List["Event"]] = Relationship(back_populates="user")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str