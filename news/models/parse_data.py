import sqlalchemy as _sql
from config import database as _database
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship


class ParseData(_database.Base):
    __tablename__ = 'parse_data'

    id = _sql.Column(_sql.Integer, primary_key=True)
    url_list = _sql.Column(_sql.String(255), nullable=False)
    html_tag_list = _sql.Column(_sql.String(255), nullable=False)
    html_attr_list = _sql.Column(_sql.String(255), nullable=False)
    html_tag_element = _sql.Column(_sql.String(255), nullable=False)
    html_attr_element_type = _sql.Column(_sql.String(255), nullable=False)
    html_attr_element_value = _sql.Column(_sql.String(255), nullable=False)
    type_url = _sql.Column(ENUM('rss', 'html', 'api', name='type_url_enum'), nullable=False, default='html')
    to_dataset = _sql.Column(_sql.Boolean, nullable=False, default=False)
    default_class_news = _sql.Column(_sql.String(255))
    name = _sql.Column(_sql.String(255))

    users = relationship("User", secondary='user_parse_data', back_populates="parse_data")
    news = relationship("News", back_populates="parse_data")