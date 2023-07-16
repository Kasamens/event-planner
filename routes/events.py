from fastapi import APIRouter, Body, HTTPException, status, Depends, Request
from models.mongo_events import Event, EventUpdate
from typing import List
from database.connection import get_session
from sqlmodel import select
from beanie import PydanticObjectId
from database.mongo_connection import Database

event_router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)



# @event_router.get("/", response_model=List[Event])
# async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
#     statement = select(Event)
#     events = session.exec(statement).all()
#     return events

# @event_router.get("/{id}", response_model=Event)
# async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
#     event = session.get(Event,id)
#     if event:
#         return event
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#          detail="Event with supplied ID does not exist"
#     )

# @event_router.post("/new")
# async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
#     session.add(new_event)
#     session.commit()
#     session.refresh(new_event)
#     return {
#         "message" : "Event created successfully"
#     }

# @event_router.put("/{id}", response_model=Event)
# async def update_event(id: int, new_event: EventUpdate, session=Depends(get_session)) -> Event:
#     event = session.get(Event,id)
#     if event:
#         event_data = new_event.dict(exclude_unset=True)
#         for key, value in event_data.items():
#             setattr(event, key, value)
#         session.add(event)
#         session.commit()
#         session.refresh(event)

#         return event
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Event with supplied ID does not exist"
#     )

# @event_router.delete("/{id}")
# async def delete_event(id: int, session=Depends(get_session)) -> dict:
#     event = session.get(Event,id)
#     if event:
#         session.delete(event)
#         session.commit()
#         return { "message" : "Event deleted successfully"}

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Event with the supplied ID not found"
#     )

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event

@event_router.post("/new")
async def create_event(body: Event) -> dict:
    await event_database.save(body)
    return {
        "message": "Event created successfully"
}

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
)
    return {
    "message": "Event deleted successfully."
}