from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from openstadia_hub.core.database import Base


class ServerInvite(Base):
    __tablename__ = "server_invites"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    token: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    activated: Mapped[bool] = mapped_column(default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    activated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    server_id: Mapped[int] = mapped_column(ForeignKey("servers.id"), nullable=False)
    activated_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
