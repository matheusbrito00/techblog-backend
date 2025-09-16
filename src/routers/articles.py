from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.schemas.schemas import ArticleBase, UserBase, CommentBase, ArticleForm, CommentForm
from src.infra.config.database import get_db
from src.infra.repositories.article import ArticleRepository
from src.infra.repositories.comment import CommentRepository
from src.routers.utils import get_logged_user

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ArticleBase)
async def create(article: ArticleForm, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    created_article = ArticleRepository(session).create(article, user.id)
    return created_article

@router.get("", response_model=List[ArticleBase])
async def read(tag_ids: Optional[List[int]] = Query(None, description="Filtro por tags usando tag_ids"), session: Session = Depends(get_db)):
    if tag_ids:
        articles = ArticleRepository(session).get_by_tags(tag_ids)
    else:
        articles = ArticleRepository(session).get()
        
    return articles

@router.get("/{article_id}", response_model=ArticleBase)
async def read_by_id(article_id: int, session: Session = Depends(get_db)):
    article = ArticleRepository(session).get_by_id(article_id)
    return article

@router.put("/{article_id}", response_model=ArticleBase)
async def update(article_id: int, article: ArticleBase, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    article_old = ArticleRepository(session).get_by_id(article_id)
    
    if not article_old:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if article_old.user_id != user.id or not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    ArticleRepository(session).update(article_id, article)
    return {
        "id": article_id,
        **article.model_dump()
    }

@router.delete("/{article_id}")
async def delete(article_id: int, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    article_old = ArticleRepository(session).get_by_id(article_id)
    
    if not article_old:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    if article_old.user_id != user.id or not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    ArticleRepository(session).delete(article_id)
    return { "message": "Article deleted successfully" }

# COMMENTS
@router.get("/{article_id}/comments", response_model=List[CommentBase])
async def read_comments(article_id: int, session: Session = Depends(get_db)):
    comments = CommentRepository(session).get(article_id)
    return comments

@router.post("/{article_id}/comments", response_model=CommentBase)
async def create_comments(article_id: int, comment: CommentForm, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    created_comment = CommentRepository(session).create(article_id, comment, user.id)
    return created_comment