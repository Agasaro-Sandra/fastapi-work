import random
from faker import Faker
from ..db.database import Base, SessionLocal, engine
from .models import Client, Room
import logging

logging.basicConfig(level=logging.INFO)

fake = Faker()

def get_room_ids(session):
    return [room.id for room in session.query(Room).all()]
    
def generate_data(num_records):
    session = SessionLocal()
    room_ids = get_room_ids(session)

    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = fake.phone_number()
        room_choice_id = random.choice(room_ids + [None])
        
        client = Client(
            first_name=first_name, 
            last_name=last_name, 
            phone_number=phone_number, 
            email=email, 
            room_choice_id=room_choice_id
        )

        session.add(client)

    session.commit()    
    session.close()
    print(f"Data generation of {num_records} clients complete!")

if __name__ == "__main__":

    Base.metadata.create_all(engine)
    generate_data(500000)