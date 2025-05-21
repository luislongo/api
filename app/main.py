from fastapi import FastAPI
from fastapi import Body, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine
from sqlalchemy.orm import Session
from .database import get_db
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

while True:
    try: 
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='night1993',
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print('Database connection successful')
        break
    except Exception as e:
        print("Unable to connect to the database")
        print(e)

        wait_time = 5
        print(f"Retrying in {wait_time} seconds...")
        time.sleep(wait_time)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.get("/posts", response_model=list[schemas.GetPostResponse],)
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/latest", response_model=schemas.GetLatestPostResponse)
async def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    if post:
        return post
    
    raise HTTPException(status_code=404, detail="No posts found")

@app.get("/posts/{post_id}", response_model=schemas.GetPostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        return post
    
    raise HTTPException(status_code=404, detail=f"Post {post_id} not found")

@app.post("/posts", response_model=schemas.CreatePostResponse, status_code=201)
async def create_post(post: schemas.CreatePostPayload, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    
    db.refresh(new_post)

    return new_post

@app.put("/posts/{post_id}", response_model=schemas.UpdatePostResponse)
async def update_post(post_id: int, post: schemas.UpdatePostPayload, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    
    post_to_update = post_query.first()

    if not post_to_update:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    updated_post = post_query.first()

    return updated_post

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).delete(synchronize_session=False)
    db.commit()

    if post:
        return {"message": f"Post {post_id} deleted successfully"}
    
    raise HTTPException(status_code=404, detail=f"Post {post_id} not found")

@app.post("/users", response_model=schemas.CreateUserResponse)
async def create_user(user: schemas.CreateUserPayload, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user
            