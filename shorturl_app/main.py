from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, declarative_base
from sqlalchemy import  Column, Integer, String, Boolean
from pydantic import BaseModel, HttpUrl
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
import string
import random

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/shorturl_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
class URLItem(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, unique=True, index=True)
    full_url = Column(String)

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
class URLCreate(BaseModel):
    url: HttpUrl

def gen_id(id_len=7):
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choices(alphabet, k=id_len))


#-------------------
# APP METHODS
#-------------------

@app.post("/shorten")
def post_shorten_url(item: URLCreate,
                sess: Session = Depends(_start_session)):
    for _ in range(20):
        short_id = gen_id()
        try:
            new_link = URLItem(short_id=short_id, full_url=str(item.url))
            sess.add(new_link)
            sess.commit()
            sess.refresh(new_link)
            return {'short_url': f'http://localhost:8000/{short_id}'}
        except:
            raise HTTPException(status_code=500, detail="Something went wrong, please try again")

@app.get("/{short_id}")
def get_full_url(short_id: str,
                     sess: Session = Depends(_start_session)):
    url_item = (
        sess.query(URLItem)
            .filter(URLItem.short_id == short_id)
            .first()
    )
    if url_item:
        return RedirectResponse(url=str(url_item.full_url), status_code=302)
    raise HTTPException(status_code=404, detail="Short url not found")



@app.get("/stats/{short_id}")
def get_stats(short_id: str,
              sess: Session = Depends(_start_session)):
    url_item = (
        sess.query(URLItem)
            .filter(URLItem.short_id == short_id)
            .first()
    )
    if url_item:
        return {
            'short_id': url_item.short_id,
            'full_url': url_item.full_url
        }
    raise HTTPException(status_code=404, detail="Short url not found")

