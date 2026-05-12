"""Create regions, readings, alerts, users tables

Revision ID: c22cada24ecf
Revises:
Create Date: 2026-05-06 15:51:45.772953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = 'c22cada24ecf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')

    op.create_table(
        'regions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('geom', Geometry('POLYGON', srid=4326), nullable=False),
        sa.Column('threshold_green', sa.Float(), server_default='30.0'),
        sa.Column('threshold_yellow', sa.Float(), server_default='50.0'),
        sa.Column('threshold_orange', sa.Float(), server_default='100.0'),
        sa.Column('threshold_red', sa.Float(), server_default='150.0'),
    )

    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('region', sa.String(100), nullable=False),
        sa.Column('level', sa.String(20), nullable=False),
        sa.Column('rain_mm', sa.Float(), nullable=True),
        sa.Column('river', sa.String(100), nullable=True),
        sa.Column('river_level_m', sa.Float(), nullable=True),
        sa.Column('sources', sa.String(500), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'readings',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('region', sa.String(100), nullable=False),
        sa.Column('rain_mm', sa.Float(), nullable=True),
        sa.Column('river_level_m', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('telegram_id', sa.BigInteger(), unique=True, nullable=False),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('cidade', sa.String(100), nullable=False),
        sa.Column('bairro', sa.String(100), nullable=True),
        sa.Column('active', sa.Boolean(), server_default='true'),
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('readings')
    op.drop_table('alerts')
    op.drop_table('regions')
    op.execute('DROP EXTENSION IF EXISTS postgis')
