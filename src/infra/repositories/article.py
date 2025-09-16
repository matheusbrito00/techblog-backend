from typing import List
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.models import models

class ArticleRepository():
    def __init__(self, session: Session):
       self.session = session
    
    def create(self, article: schemas.ArticleBase, user_id: int):
        tag_ids = article.tag_ids  # lista de IDs vinda do request
        tags = self.session.query(models.Tag).filter(models.Tag.id.in_(tag_ids)).all()
        
        article_db = models.Article(title=article.title,
                                    image=article.image,
                                    content=article.content,
                                    tags=tags,
                                    user_id=user_id)
        
        self.session.add(article_db)
        self.session.commit()
        self.session.refresh(article_db)

        return article_db
    
    def get(self):
        stmt = select(models.Article)
        articles = self.session.execute(stmt).scalars().all()
        
        return articles
    
    def get_by_id(self, article_id: int):
        stmt = select(models.Article).where(
            models.Article.id == article_id
        )
        article = self.session.execute(stmt).scalars().first()
        
        return article
    
    def get_by_tags(self, tag_ids: List[int]):
        stmt = select(models.Article).join(models.Article.tags).filter(
            models.Tag.id.in_(tag_ids)
        ).distinct()
        articles = self.session.execute(stmt).scalars().all()
        
        return articles
    
    def update(self, article_id: int, article: schemas.ArticleBase):
        stmt_tags = select(models.Tag).filter(models.Tag.id.in_(article.tag_ids))
        tags = self.session.execute(stmt_tags).all()
        
        stmt_article = update(models.Article).where(
            models.Article.id == article_id
        ).values(title=article.title,
                 image=article.image,
                 content=article.image,
                 tags=tags)
        
        self.session.execute(stmt_article)
        self.session.commit()
        
    def delete(self, article_id: int):
        stmt = delete(models.Article).where(models.Article.id == article_id)
        
        self.session.execute(stmt)
        self.session.commit()
    