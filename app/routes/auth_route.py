from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import user_models
from app.schemas import auth_schema
from app.adapters import users_adapter

router = APIRouter(tags=["auth"])

@router.post("/login")
async def login(payload: auth_schema.LoginPayload, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not users_adapter.verify(payload.password, user.public_key):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {"message": "Login successful", "user_id": user.id}