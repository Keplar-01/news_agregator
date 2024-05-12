import sqlalchemy as _sql
from config import database as _database
from sqlalchemy import ForeignKey
import datetime as _dt

class News(_database.Base):
    __tablename__ = 'news'

    id = _sql.Column(_sql.Integer, primary_key=True)
    parse_data_id = _sql.Column(_sql.Integer, ForeignKey('parse_data.id'))  # новый столбец
    text = _sql.Column(_sql.Text, nullable=False)
    title = _sql.Column(_sql.VARCHAR(255), nullable=False)
    url = _sql.Column(_sql.VARCHAR(255), nullable=False, unique=True)
    is_train = _sql.Column(_sql.Boolean, nullable=False, default=False)
    classes = _sql.Column(_sql.VARCHAR(255))
    name_source = _sql.Column(_sql.VARCHAR(255))
    date = _sql.Column(_sql.DateTime, default=_dt.datetime.now())