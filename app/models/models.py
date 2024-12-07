from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..db.database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String(255),index=True)
    last_name = Column(String(255),index=True)
    email = Column(String(255), unique=False, index=True)
    phone_number = Column(String(255), unique=False, index=True)
    room_choice_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room", back_populates="clients")

    @property
    def room_choice(self):
        if self.room:
            return self.room.room_type
        
        return None
    
    @room_choice.setter
    def room_choice(self, value: str):
        self.room_choice_id = value
    
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer,primary_key=True,index=True)
    room_type = Column(String(255),index=True, unique=True)
    room_description = Column(String(255), index=True)
    clients = relationship("Client", back_populates="room")
