from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from openstadia_hub.core.database import Base


class App(Base):
    __tablename__ = "apps"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    command: Mapped[str]
    server_id: Mapped[int] = mapped_column(ForeignKey("servers.id"))

    server: Mapped["Server"] = relationship(back_populates="apps")
