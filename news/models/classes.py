import sqlalchemy as _sql
from config import database as _database

from models.news import News
from models.user import User

from models.user import user_classes
from sqlalchemy.orm import relationship


class Classes(_database.Base):
    __tablename__ = 'classes'

    id = _sql.Column(_sql.Integer, primary_key=True)
    name = _sql.Column(_sql.String(255), nullable=False)
    description = _sql.Column(_sql.String(255), nullable=False)
    is_active = _sql.Column(_sql.Boolean, default=False, nullable=False)

    users = relationship("User", secondary=user_classes, back_populates="classes")
    news = relationship("News", back_populates="classes")
