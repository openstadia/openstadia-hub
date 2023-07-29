from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from openstadia_hub.core.database import Base


class ServerAccess(Base):
    __tablename__ = "server_accesses"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    server_id: Mapped[int] = mapped_column(ForeignKey("servers.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="server_accesses")
    server: Mapped["Server"] = relationship(back_populates="server_accesses")
