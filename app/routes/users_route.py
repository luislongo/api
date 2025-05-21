
from app import models, schemas
from app.adapters import adapters
from app.database import get_db
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users", response_model=schemas.CreateUserResponse)
async def create_user(user: schemas.CreateUserPayload, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = adapters.hash(user)

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user

@router.get("/users/{user_id}", response_model=schemas.UserBaseResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user:
        return user
    
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

