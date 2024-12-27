from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, declarative_base
from sqlalchemy import  Column, Integer, String, Boolean
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends


SQLALCHEMY_DATABASE_URL = "sqlite:///./data/todo_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
class TodoTable(Base):
    __tablename__ = 'todo_notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, nullable=False)

# создаем таблицу
Base.metadata.create_all(bind=engine)

app = FastAPI()

def _start_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# DATA VALIDATION
class TodoInsert(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoTableDQ(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        from_attributes = True

#-------------------
# APP METHODS
#-------------------

# POST
@app.post("/items", response_model=TodoTableDQ)
def insert_item(item: TodoInsert,
                session: Session = Depends(_start_session)):
    row = TodoTable(
        title=item.title,
        description=item.description,
        completed=item.completed
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

# GET all items
@app.get("/items", response_model=List[TodoTableDQ])
def get_items(session: Session = Depends(_start_session)):
    return session.query(TodoTable).all()

#GET items by id
@app.get("/items/{item_id}", response_model=TodoTableDQ)
def get_items_by_id(id: int,
                    session: Session = Depends(_start_session)):
    row = (session.query(TodoTable)
                  .filter(TodoTable.id == id)
                  .first()
    )
    if row:
        return row
    raise HTTPException(status_code=404, detail=f"Item id = {id} not found")


#PUT items by id
@app.put("/items/{item_id}", response_model=TodoTableDQ)
def get_items_by_id(id: int,
                    session: Session = Depends(_start_session)):
    ret_val = (session.query(TodoTable)
                  .filter(TodoTable.id == id)
                  .first()
    )
    if ret_val:
        ret_val.title = TodoTable.title
        ret_val.description = TodoTable.description
        ret_val.completed = TodoTable.completed
        session.commit()
        session.refresh(ret_val)
        return ret_val
    raise HTTPException(status_code=404, detail=f"Item id = {id} not found")


#DELETE all rows from "todo_notes" table
@app.delete("/items/{item_id}")
def delete_item(id: int,
                session: Session = Depends(_start_session)):
    ret_val = (session.query(TodoTable)
                  .filter(TodoTable.id == id)
                  .first()
    )
    if ret_val:
        session.delete(ret_val)
        session.commit()
        return {"message": f"item with id {id} was deleted from database successfully"}
    raise HTTPException(status_code=404, detail=f"Item id = {id} not found")

@app.delete("/items")
def delete_db(session: Session = Depends(_start_session)):
    import shutil
    import datetime
    timestamp  = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    shutil.copy2('./data/todo_app.db',f'./data/todo_app_{timestamp}.db')

    session.query(TodoTable).delete()
    session.commit()
    return {"message": "All data from app was deleted"}