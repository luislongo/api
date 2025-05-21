
from app import schemas
from app.database import get_db
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.models import post_models

router = APIRouter()

@router.get("/posts", response_model=list[schemas.GetPostResponse],)
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(post_models.Post).all()
    return posts

@router.get("/posts/latest", response_model=schemas.GetLatestPostResponse)
async def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(post_models.Post).order_by(post_models.Post.created_at.desc()).first()
    if post:
        return post
    
    raise HTTPException(status_code=404, detail="No posts found")

@router.get("/posts/{post_id}", response_model=schemas.GetPostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(post_models.Post).filter(post_models.Post.id == post_id).first()
    if post:
        return post
    
    raise HTTPException(status_code=404, detail=f"Post {post_id} not found")

@router.post("/posts", response_model=schemas.CreatePostResponse, status_code=201)
async def create_post(post: schemas.CreatePostPayload, db: Session = Depends(get_db)):
    new_post = post_models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    
    db.refresh(new_post)

    return new_post

@router.put("/posts/{post_id}", response_model=schemas.UpdatePostResponse)
async def update_post(post_id: int, post: schemas.UpdatePostPayload, db: Session = Depends(get_db)):
    post_query = db.query(post_models.Post).filter(post_models.Post.id == post_id)
    
    post_to_update = post_query.first()

    if not post_to_update:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    updated_post = post_query.first()

    return updated_post

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(post_models.Post).filter(post_models.Post.id == post_id).delete(synchronize_session=False)
    db.commit()

    if post:
        return {"message": f"Post {post_id} deleted successfully"}
    
    raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
