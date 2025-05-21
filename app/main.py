import psycopg2
import time
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine

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

from .routes import posts_route, users_route, root_route
app.include_router(root_route.router)
app.include_router(posts_route.router)
app.include_router(users_route.router)