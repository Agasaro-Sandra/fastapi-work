from pydantic import BaseModel
from typing import Optional

class ClientBase(BaseModel):
    id: Optional[int]
    email: Optional[str] 
    phone_number: Optional[str] 
    first_name: Optional[str] 
    last_name: Optional[str] 
    room_choice: Optional[str] 
    
    class Config:
        orm_model = True


class ClientCreate(ClientBase):
    pass 

class ClientUpdate(ClientBase):
    pass

class RoomBase(BaseModel):
    id: int
    room_type: Optional[str] 
    room_description: Optional[str] 

    class Config: 
        orm_model = True

class RoomCreate(RoomBase):
    pass


    