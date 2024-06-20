import sqlalchemy as _sql
from config import database as _database
from sqlalchemy import Table, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

# Определение связующей таблицы
user_classes = Table('user_classes', _database.Base.metadata,
    _sql.Column('user_id', _sql.Integer, ForeignKey('users.id')),
    _sql.Column('class_id', _sql.Integer, ForeignKey('classes.id'))
)

user_parse_data = Table('user_parse_data', _database.Base.metadata,
    _sql.Column('user_id', _sql.Integer, ForeignKey('users.id')),
    _sql.Column('parse_data_id', _sql.Integer, ForeignKey('parse_data.id'))
)

class User(_database.Base):
    __tablename__ = 'users'

    id = _sql.Column(_sql.Integer, primary_key=True)
    name = _sql.Column(_sql.String(255), nullable=True)
    email = _sql.Column(_sql.String(255), nullable=False)
    password = _sql.Column(_sql.String(255), nullable=False)
    created_at = _sql.Column(_sql.DateTime, default=_sql.func.now())
    role = _sql.Column(ENUM('admin', 'user', 'checker',name='role_enum'), nullable=False, default='user')

    classes = relationship("Classes", secondary=user_classes, back_populates="users")
    parse_data = relationship("ParseData", secondary=user_parse_data, back_populates="users")