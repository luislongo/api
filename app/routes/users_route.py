
from app.schemas import user_schema
from app.adapters import users_adapter
from app.database import get_db
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import user_models

router = APIRouter(prefix='/users', tags=["users"])

@router.post("/", response_model=user_schema.CreateUserResponse)
async def create_user(user: user_schema.CreateUserPayload, db: Session = Depends(get_db)):

    existing_user = db.query(user_models.User).filter(user_models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    pwd_hash = users_adapter.hash(user.password)

    new_user = user_models.User(
        email=user.email,
        public_key=pwd_hash,
     )

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user

@router.get("/{user_id}", response_model=user_schema.UserBaseResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    
    if user:
        return user
    
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

