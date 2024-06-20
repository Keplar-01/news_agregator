import sqlalchemy as _sql
from config import database as _database

from models.news import News
from models.user import User

from models.user import user_classes
from sqlalchemy.orm import relationship


class MlModel(_database.Base):
    __tablename__ = 'ml_models'

    id = _sql.Column(_sql.Integer, primary_key=True)
    name = _sql.Column(_sql.String(255), nullable=False)
    path_model = _sql.Column(_sql.String(255), nullable=False)
    path_encoder = _sql.Column(_sql.String(255), nullable=True)
    path_tokenizer = _sql.Column(_sql.String(255), nullable=True)
    path_sub_model = _sql.Column(_sql.String(255), nullable=True)
    type = _sql.Column(_sql.String(255), nullable=False)
    is_active = _sql.Column(_sql.Boolean, default=False)