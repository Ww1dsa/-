from sqlalchemy import Column, DateTime, Integer, String, Text, func

from .database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    contact = Column(String(120), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class ForumPost(Base):
    __tablename__ = "forum_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(80), nullable=False, default="匿名用户")
    reply_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
