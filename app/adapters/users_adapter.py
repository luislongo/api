from app import schemas
from app.models import user_models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(user: schemas.CreateUserPayload):
    pwd_hash = pwd_context.hash(user.password)
    new_user = user_models.User(
        email=user.email,
        public_key=pwd_hash
    )
    
    return new_user
