from app.schemas import user_schema 
from app.models import user_models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    pwd_hash = pwd_context.hash(password)
    return pwd_hash

def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)