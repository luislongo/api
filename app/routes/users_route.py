
from app.schemas import user_schema
from app.adapters import users_adapter
from app.database import get_db
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import user_models

router = APIRouter()

@router.post("/users", response_model=user_schema.CreateUserResponse)
async def create_user(user: user_schema.CreateUserPayload, db: Session = Depends(get_db)):
    existing_user = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = users_adapter.hash(user)

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user

@router.get("/users/{user_id}", response_model=user_schema.UserBaseResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    
    if user:
        return user
    
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

