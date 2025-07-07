"""Initial schema

Revision ID: init123
Revises: 
Create Date: 2025-07-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'init123'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_devices_id'), 'devices', ['id'], unique=False)
    op.create_index(op.f('ix_devices_device_name'), 'devices', ['device_name'], unique=True)

    op.create_table('results',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('average_before', sa.Float(), nullable=True),
        sa.Column('average_after', sa.Float(), nullable=True),
        sa.Column('data_size', sa.Integer(), nullable=True),
        sa.Column('created_date', sa.DateTime(), nullable=True),
        sa.Column('updated_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_results_id'), 'results', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_results_id'), table_name='results')
    op.drop_table('results')
    op.drop_index(op.f('ix_devices_device_name'), table_name='devices')
    op.drop_index(op.f('ix_devices_id'), table_name='devices')
    op.drop_table('devices')
