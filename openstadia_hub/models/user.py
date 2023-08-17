from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from openstadia_hub.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    auth_id: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    servers: Mapped[List["Server"]] = relationship(back_populates="owner")

    server_accesses: Mapped[List["ServerAccess"]] = relationship(back_populates="user")
