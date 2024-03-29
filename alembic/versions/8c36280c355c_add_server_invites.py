"""Add server invites

Revision ID: 8c36280c355c
Revises: b10b1ee3e7a7
Create Date: 2023-11-30 10:56:10.015071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c36280c355c'
down_revision: Union[str, None] = 'b10b1ee3e7a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('server_invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('activated', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('expiration_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('activated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('server_id', sa.Integer(), nullable=False),
    sa.Column('activated_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activated_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['server_id'], ['servers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_server_invites_id'), 'server_invites', ['id'], unique=False)
    op.create_index(op.f('ix_server_invites_token'), 'server_invites', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_server_invites_token'), table_name='server_invites')
    op.drop_index(op.f('ix_server_invites_id'), table_name='server_invites')
    op.drop_table('server_invites')
    # ### end Alembic commands ###
