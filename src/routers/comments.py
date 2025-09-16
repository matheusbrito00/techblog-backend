from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.schemas.schemas import UserBase, CommentBase
from src.infra.config.database import get_db
from src.infra.repositories.comment import CommentRepository
from src.routers.utils import get_logged_user

router = APIRouter(prefix="/comments", tags=["Comments"], dependencies=[Depends(get_logged_user)])

@router.get("/{comment_id}", response_model=CommentBase)
async def read_by_id(comment_id: int, session: Session = Depends(get_db)):
    comment = CommentRepository(session).get_by_id(comment_id)
    
    return comment

@router.put("/{comment_id}", response_model=CommentBase)
async def update(comment_id: int, comment: CommentBase, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    comment_old = CommentRepository(session).get_by_id(comment_id)
    
    if not comment_old:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if comment_old.user_id != user.id or not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    CommentRepository(session).update(comment_id, comment)
    return {
        "id": comment_id,
        **comment.model_dump()
    }

@router.delete("/{comment_id}")
async def delete(comment_id: int, user: UserBase = Depends(get_logged_user), session: Session = Depends(get_db)):
    comment_old = CommentRepository(session).get_by_id(comment_id)
    
    if not comment_old:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if comment_old.user_id != user.id or not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    CommentRepository(session).delete(comment_id)
    return { "message": "Comment deleted successfully" }