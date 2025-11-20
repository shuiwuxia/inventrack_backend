# File: routes/consumer_auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from .. import schemas, models
from ..dependencies import get_db

router = APIRouter(
    prefix="/consumer/auth",
    tags=['Consumer Authentication']
)

DBDependency = Annotated[Session, Depends(get_db)]

@router.post("/register", response_model=schemas.Consumer, status_code=status.HTTP_201_CREATED)
def register_consumer(request: schemas.ConsumerCreate, db: DBDependency):
    """
    Registers a new consumer user by saving details to the 'consumers' table.
    """

    # ✅ 1. Check if email already exists
    existing_consumer = db.query(models.Consumer).filter(
        models.Consumer.email_id == request.email_id
    ).first()

    if existing_consumer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Consumer with email '{request.email_id}' already registered."
        )

    # ✅ 2. Create consumer (PLAIN PASSWORD as per your project)
    new_consumer = models.Consumer(
        full_name=request.full_name,
        email_id=request.email_id,
        phone_number=request.phone_number,
        address=request.address,
        password_hash=request.password  # ✅ storing plaintext
    )

    db.add(new_consumer)
    db.commit()
    db.refresh(new_consumer)

    return new_consumer
