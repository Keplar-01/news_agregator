"""create_table_parse_data

Revision ID: fa194640ba54
Revises: 
Create Date: 2024-05-10 12:30:43.797439

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = '<new_revision_id>'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # create parse_data table
    op.create_table(
        'parse_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_list', sa.String(255), nullable=False),
        sa.Column('html_tag_list', sa.String(255), nullable=False),
        sa.Column('html_attr_list', sa.String(255), nullable=False),
        sa.Column('html_tag_element', sa.String(255), nullable=False),
        sa.Column('html_attr_element_type', sa.String(255), nullable=False),
        sa.Column('html_attr_element_value', sa.String(255), nullable=False),
        sa.Column('type_url', ENUM('rss', 'html', 'api', name='type_url_enum'), nullable=False, server_default='html'),
        sa.Column('to_dataset', sa.Boolean, nullable=False, server_default=sa.sql.expression.false()),
        sa.Column('default_class_news', sa.String(255)),
        sa.Column('name', sa.String(255))
    )

    # create classes table
    op.create_table(
        'classes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, default=False, nullable=False)
    )

    # create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('role', ENUM('admin', 'user', 'checker', name='role_enum'), nullable=False, server_default='user')
    )

    # create news table
    op.create_table(
        'news',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('parse_data_id', sa.Integer, sa.ForeignKey('parse_data.id')),
        sa.Column('text', sa.String(150000), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('url', sa.String(255), nullable=False, unique=True),
        sa.Column('is_train', sa.Boolean, nullable=False, server_default=sa.sql.expression.false()),
        sa.Column('classes_id', sa.Integer, sa.ForeignKey('classes.id'), nullable=True),
        sa.Column('mood', sa.String(255), nullable=True),
        sa.Column('name_source', sa.String(255)),
        sa.Column('date', sa.DateTime, server_default=sa.func.now())
    )

    # create user_classes table
    op.create_table(
        'user_classes',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('class_id', sa.Integer, sa.ForeignKey('classes.id'))
    )

    # create user_parse_data table
    op.create_table(
        'user_parse_data',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('parse_data_id', sa.Integer, sa.ForeignKey('parse_data.id'))
    )

    op.create_table(
        'ml_models',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('path_model', sa.String(255), nullable=False),
        sa.Column('path_encoder', sa.String(255), nullable=True),
        sa.Column('path_tokenizer', sa.String(255), nullable=True),
        sa.Column('path_sub_model', sa.String(255), nullable=True),
        sa.Column('type', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, default=False)
    )

def downgrade():
    op.drop_table('news')
    op.drop_table('users')
    op.drop_table('user_parse_data')
    op.drop_table('user_classes')
    op.drop_table('classes')
    op.drop_table('parse_data')
    op.drop_table('ml_models')