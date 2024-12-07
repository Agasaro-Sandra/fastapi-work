from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import models, schema
from app.db.database import SessionLocal, engine
from app.routers import route

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


@app.post("/clients",response_model=schema.ClientBase)
def post_client(client:schema.ClientCreate, db:Session=Depends(get_db)):
    return route.create_client(db=db, client=client)

@app.get("/clients", response_model=list[schema.ClientBase])
def get_clients_route(db: Session = Depends(get_db)):
    clients = route.get_clients(db)  # Fetch all clients without pagination

    if not clients:
        raise HTTPException(status_code=404, detail="No clients available")

    return clients


@app.get("/clients/{client_id}",response_model=schema.ClientBase)
def get_client(client_id:int, db:Session=Depends(get_db)):
    db_client = route.get_client_by_id(db,client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="client not found")
    return db_client

@app.put("/clients/{client_id}")
def update_client_route(client_id: int,  client: schema.ClientUpdate, db: Session = Depends(get_db)):
    return route.update_client(db, client_id, client)

@app.delete("/clients/{client_id}")
def delete_client_route(client_id:int, db: Session = Depends(get_db)):
    return route.delete_client(db, client_id)



@app.get("/rooms", response_model=list[schema.RoomBase])
def get_rooms(skip:int=0, limit:int=500000, db:Session=Depends(get_db)):
    rooms = route.get_rooms(db,skip=skip,limit=limit)
    return rooms