from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class CreateUserPayload(UserBase):
    password: str

class UserBaseResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CreateUserResponse(UserBaseResponse):
    pass

class GetUserResponse(UserBaseResponse):
    pass