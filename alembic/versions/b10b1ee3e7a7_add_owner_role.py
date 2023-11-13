"""Add owner role

Revision ID: b10b1ee3e7a7
Revises: 0828b34df47b
Create Date: 2023-11-12 12:22:07.426970

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.orm import Session

from openstadia_hub.crud.server import get_servers
from openstadia_hub.crud.server_access import create_server_access, delete_server_access, UserServerRole

# revision identifiers, used by Alembic.
revision: str = 'b10b1ee3e7a7'
down_revision: Union[str, None] = '0828b34df47b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    for server in get_servers(session):
        create_server_access(session, user_id=server.owner_id, server_id=server.id, role=UserServerRole.OWNER)


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    for server in get_servers(session):
        delete_server_access(session, user_id=server.owner_id, server_id=server.id)
