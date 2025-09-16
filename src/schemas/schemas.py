from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserSignIn(BaseModel):
    mail: str
    password: str

class UserBase(BaseModel):
    id: Optional[int] = None
    mail: str
    name: str
    password: str
    isAdmin: Optional[bool] = False
    
    class Config:
        from_attributes = True

class TagBase(BaseModel):
    id: Optional[int] = None
    name: str
    
    class Config:
        from_attributes = True
   
class CommentForm(BaseModel):
    content: str
    parent_id: Optional[int] = None
        
class CommentBase(BaseModel):
    id: Optional[int] = None
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    article_id: int
    user_id: Optional[int]
    user: Optional[UserBase]
    parent_id: Optional[int] = None
    replies: Optional[List["CommentBase"]] = [] 
    
    class Config:
        from_attributes = True
      
class ArticleForm(BaseModel):
    title: str
    image: Optional[str] = None
    content: str
    tag_ids: List[int] = []
      
class ArticleBase(BaseModel):
    id: Optional[int] = None
    title: str
    image: Optional[str] = None
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None
    tag_ids: List[int] = []
    tags: Optional[List[TagBase]] = []
    comments: Optional[List[CommentBase]] = []
    user_id: int
    user: Optional[UserBase]
    
    class Config:
        from_attributes = True
        
class LoginSuccess(BaseModel):
    user: UserBase
    access_token: str
    refresh_token: Optional[str] = None
    
CommentBase.model_rebuild()