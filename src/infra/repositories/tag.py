from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.models import models

class TagRepository():
    def __init__(self, session: Session):
        self.session = session
        
    def create(self, tag: schemas.TagBase):
        tag_db = models.Tag(name=tag.name)
        
        self.session.add(tag_db)
        self.session.commit()
        self.session.refresh(tag_db)
    
    def get(self):
        stmt = select(models.Tag)
        tags = self.session.execute(stmt).scalars().all()
        
        return tags
    
    def get_by_id(self, tag_id: int):
        stmt = select(models.Tag).where(
            models.Tag.id == tag_id
        )
        tag = self.session.execute(stmt).scalars().first()
        return tag
    
    def update(self, tag_id: int, tag: schemas.TagBase):
        stmt = update(models.Tag).where(
            models.Tag.id == tag_id
        ).values(name=tag.name)
        
        self.session.execute(stmt)
        self.session.commit()
        
    def delete(self, tag_id: int):
        stmt = delete(models.Tag).where(models.Tag.id == tag_id)
        
        self.session.execute(stmt)
        self.session.commit()