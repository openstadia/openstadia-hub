from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from openstadia_hub.core.database import Base
from openstadia_hub.schemas.user_server_role import UserServerRole


class ServerAccess(Base):
    __tablename__ = "server_accesses"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    server_id: Mapped[int] = mapped_column(ForeignKey("servers.id"), primary_key=True)
    role: Mapped[UserServerRole] = mapped_column(Enum(UserServerRole), nullable=False)

    user: Mapped["User"] = relationship(back_populates="server_accesses")
    server: Mapped["Server"] = relationship(back_populates="server_accesses")
