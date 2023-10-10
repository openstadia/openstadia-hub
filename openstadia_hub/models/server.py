from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from openstadia_hub.core.database import Base


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    token: Mapped[str] = mapped_column(unique=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="servers")
    apps: Mapped[List["App"]] = relationship(back_populates="server", cascade="all, delete")

    server_accesses: Mapped[List["ServerAccess"]] = relationship(back_populates="server")
