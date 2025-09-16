from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.models import models

class UserRepository():
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: schemas.UserBase):
        db_user = models.User(mail=user.mail,
                              name=user.name,
                              password=user.password,
                              isAdmin=user.isAdmin)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
    
    def get_by_id(self, user_id: int):
        stmt = select(models.User).where(models.User.id == user_id)
        user = self.session.execute(stmt).scalars().first()
        
        return user
    
    def get_by_mail(self, mail: str):
        stmt = select(models.User).where(models.User.mail == mail)
        return self.session.execute(stmt).scalars().first()
    
    def update(self, user_id: int, user: schemas.UserBase):
        stmt = update(models.User).where(
            models.User.id == user_id
        ).values(mail=user.mail,
                 name=user.name,
                 isAdmin=user.isAdmin)
        self.session.execute(stmt)
        self.session.commit()
        
    def delete(self, user_id: int):
        stmt = delete(models.User).where(models.User.id == user_id)
        
        self.session.execute(stmt)
        self.session.commit()