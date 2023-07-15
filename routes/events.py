from fastapi import APIRouter, Body, HTTPException, status, Depends, Request
from models.events import Event, EventUpdate
from typing import List
from database.connection import get_session
from sqlmodel import select

event_router = APIRouter(
    tags=["Events"]
)

events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event,id)
    if event:
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
         detail="Event with supplied ID does not exist"
    )

@event_router.post("/new")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {
        "message" : "Event created successfully"
    }

@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return { "message" : "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with the supplied ID not found"
    )

@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message" : "Events deleted successfully"
    }