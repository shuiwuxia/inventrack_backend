from .database import SessionLocal 
from typing import Generator
from sqlalchemy.orm import Session 
from inventrack import models
from fastapi import Depends, HTTPException, status 

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()