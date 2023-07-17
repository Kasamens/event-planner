from sqlmodel import SQLModel, JSON, Field, Column, Relationship
from typing import List, Optional
from models.users import User


class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    location: str
    tags: List[str] = Field(sa_column=Column(JSON))
    user: Optional[User] = Relationship(back_populates="events")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class EventUpdate(SQLModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]
    
