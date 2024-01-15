from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import Column, String, Integer, DateTime

from app.db.base.BaseFeat import DbBase


class SpiderDocument(DbBase):
    __tablename__ = 'spider_document'
    # 使用Mapped写法
    source: Mapped[str] = mapped_column(String,nullable=True)
    domain: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    article_url: Mapped[str] = mapped_column(String)
    read_count: Mapped[int] = mapped_column(Integer,nullable=True)
    like_count: Mapped[int] = mapped_column(Integer,nullable=True)
    comment_count: Mapped[int] = mapped_column(Integer,nullable=True)
    publish_time: Mapped[DateTime] = mapped_column(DateTime)
    behot_time: Mapped[DateTime] = mapped_column(DateTime,nullable=True)








