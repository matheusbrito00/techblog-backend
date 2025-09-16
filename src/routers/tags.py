from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.schemas import TagBase, UserBase
from src.infra.config.database import get_db
from src.infra.repositories.tag import TagRepository
from src.routers.utils import get_logged_user

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TagBase)
async def create(tag: TagBase, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    if not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    created_tag = TagRepository(session).create(tag)
    return created_tag

@router.get("", response_model=List[TagBase])
async def read(session: Session = Depends(get_db)):
    tags = TagRepository(session).get()
    return tags

@router.get("/{tag_id}", response_model=TagBase)
async def read_by_id(tag_id: int, session: Session = Depends(get_db)):
    tag = TagRepository(session).get_by_id(tag_id)
    return tag
    
@router.put("/{tag_id}", response_model=TagBase)
async def update(tag_id: int, tag: TagBase, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    if not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    TagRepository(session).update(tag_id, tag)
    return {
        "id": tag_id,
        **tag.model_dump()
    }

@router.delete("/{tag_id}")
async def delete(tag_id: int, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    if not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    TagRepository(session).delete(tag_id)
    return { "message": "User deleted successfully" }