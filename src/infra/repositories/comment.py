from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.models import models

class CommentRepository():
    def __init__(self, session: Session):
       self.session = session
       
    def create(self, article_id: int, comment: schemas.CommentBase, user_id: int):
        comment_db = models.Comment(content=comment.content,
                                    article_id=article_id,
                                    user_id=user_id,
                                    parent_id=comment.parent_id)
        
        self.session.add(comment_db)
        self.session.commit()
        self.session.refresh(comment_db)
        
        return comment_db
         
    def get(self, article_id: int):
       stmt = select(models.Comment).where(models.Comment.article_id == article_id)
       comments = self.session.execute(stmt).scalars().all()
       
       return comments
    
    def get_by_id(self, comment_id: int):
       stmt = select(models.Comment).where(models.Comment.id == comment_id)
       comment = self.session.execute(stmt).scalars().first()
       
       return comment
    
    # def get_replies():
    #     pass
    
    def update(self, comment_id: int, comment: schemas.CommentBase):
        stmt = update(models.Comment).where(
            models.Comment.id == comment_id
        ).values(content=comment.content)
        
        self.session.execute(stmt)
        self.session.commit()
    
    def delete(self, comment_id: int):
        stmt = delete(models.Comment).where(models.Comment.id == comment_id)
        
        self.session.execute(stmt)
        self.session.commit()