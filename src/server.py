from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth, tags, articles, comments
from src.infra.config.database import create_db, SessionLocal
from contextlib import asynccontextmanager
from src.infra.models import models
from src.infra.providers import hash_provider
import json
from pathlib import Path
import os

# create_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    session = SessionLocal()
    base_path = Path(os.getenv("DATA_PATH", Path(__file__).parent.parent))
    try:
        if session.query(models.User).count() == 0:
            user_path = base_path / "users.json"
            users = json.loads(user_path.read_text(encoding="utf-8"))
            for user in users:
                user['password'] = hash_provider.generate_hash(user['password'])
                session.add(models.User(**user))
        
        if session.query(models.Tag).count() == 0:
            tag_path = base_path / "tags.json"
            tags = json.loads(tag_path.read_text(encoding="utf-8"))
            for tag in tags:
                session.add(models.Tag(**tag))
        
        if session.query(models.Article).count() == 0:
            article_path = base_path / "articles_with_tags.json"
            articles = json.loads(article_path.read_text(encoding="utf-8"))
            for article in articles:
                tag_objs = []
                for tag in article["tags"]:
                    db_tag = session.query(models.Tag).filter_by(id=tag["id"]).first()
                    if db_tag:
                        tag_objs.append(db_tag)

                article_obj = models.Article(
                    title=article["title"],
                    content=article["content"],
                    user_id=article["user_id"],
                    tags=tag_objs
                )
                session.add(article_obj)
            
        session.commit()
        yield
    finally:
        session.close()

app = FastAPI(lifespan=lifespan)

# CORS
origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)
app.include_router(tags.router)
app.include_router(articles.router)
app.include_router(comments.router)