from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Table, DateTime, func
from sqlalchemy.orm import relationship
from src.infra.config.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    mail = Column(String)
    name = Column(String)
    password = Column(String)
    isAdmin = Column(Boolean)
    articles = relationship("Article", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    
article_tag_table = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tags = relationship("Tag", secondary=article_tag_table, back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates='articles')
    image = Column(String, nullable=True)
    
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    articles = relationship("Article", secondary=article_tag_table, back_populates="tags")
    
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    article_id = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", back_populates="comments")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="comments")
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    