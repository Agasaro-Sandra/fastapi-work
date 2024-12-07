from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from typing import Optional
from ..models import models, schema

def get_client_by_id(db: Session, id:int):
    client = (
        db.query(models.Client)
        .filter(models.Client.id == id)
        .options(joinedload(models.Client.room))
        .first()
    )

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return client

def get_clients(db: Session, skip:int=0, limit:int=500000):
    return db.query(models.Client).offset(skip).limit(limit).all()

def create_client(db: Session, client:schema.ClientCreate):

    room_id = None

    if client.room_choice is None:
        room = db.query(models.Room).filter(models.Room.room_type == client.room_choice).first()
        if not room:
            raise HTTPException(status_code=404, detail=f"Room type '{client.room_choice}' not found")
        room_id = room.id

    db_client = models.Client(
        email=client.email, 
        phone_number=client.phone_number, 
        first_name=client.first_name, 
        last_name=client.last_name, 
        room_choice_id=room_id
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client

def update_client(db: Session, client_id: int, client:schema.ClientUpdate):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()

    if not db_client:
        raise HTTPException(status_code=404, detail=f"Client with id {client_id} not found")

    if client.email:
        db_client.email = client.email

    if client.phone_number:
        db_client.phone_number = client.phone_number
    
    if client.first_name:
        db_client.first_name = client.first_name

    if client.last_name:
        db_client.last_name = client.last_name

    if client.room_choice:
        
        room = db.query(models.Room).filter(models.Room.room_type == client.room_choice).first()
        if not room:
            raise HTTPException(status_code=404, detail=f"Room type '{client.room_choice}' not found")
        db_client.room_choice_id = room.id

    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()

    if not db_client:
        raise HTTPException(status_code=404, detail=f"Client witd id {client_id} not found")
    
    db.delete(db_client)
    db.commit()
    return{"message": f"Client with id {client_id} has been deleted successfully"}

def get_rooms(db: Session, skip:int=0, limit:int=500000):
    return db.query(models.Room).offset(skip).limit(limit).all()
{"presets": ["@babel/preset-env", "@babel/preset-react"]}