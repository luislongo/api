
from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePostPayload(PostBase):
    pass

class UpdatePostPayload(PostBase):
    pass

class BasePostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        
class CreatePostResponse(BasePostResponse):
    pass

class UpdatePostResponse(BasePostResponse):
    pass

class GetPostResponse(BasePostResponse):
    pass

class GetLatestPostResponse(BasePostResponse):
    pass
