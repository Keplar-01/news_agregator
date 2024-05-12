"""create_table_parse_data

Revision ID: fa194640ba54
Revises: 
Create Date: 2024-05-10 12:30:43.797439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import datetime as dt

# revision identifiers, used by Alembic.
revision: str = 'fa194640ba54'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # code to implement the upgrade
    op.create_table(
        'parse_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_list', sa.String(255), nullable=False),
        sa.Column('html_tag_list', sa.String(255), nullable=False),
        sa.Column('html_attr_list', sa.String(255), nullable=False),
        sa.Column('html_tag_element', sa.String(255), nullable=False),
        sa.Column('html_attr_element_type', sa.String(255), nullable=False),
        sa.Column('html_attr_element_value', sa.String(255), nullable=False),
        sa.Column('type_url', sa.Enum('rss', 'html', name='type_url_enum'), nullable=False, default='html'),
        sa.Column('to_dataset', sa.Boolean, nullable=False, default=False),
        sa.Column('default_class_news', sa.String(255)),
        sa.Column('name', sa.String(255), nullable=False),
    )

    op.create_table(
        'news',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('parse_data_id', sa.Integer, sa.ForeignKey('parse_data.id')),  # new column
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('url', sa.String(255), nullable=False, unique=True),
        sa.Column('is_train', sa.Boolean, nullable=False, default=False),
        sa.Column('classes', sa.String(255)),
        sa.Column('name_source', sa.String(255)),
        sa.Column('date', sa.DateTime, default=dt.datetime.now()),
    )


def downgrade():
    # code to implement the downgrade
    op.drop_table('parse_data')
    op.drop_table('news')